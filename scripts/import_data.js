const fs = require('fs');

const args = process.argv.slice(2);
if (args.length < 1) {
    console.log("Usage: node import_data.js <path_to_json> [--import]");
    console.log("  Default is DRY RUN.");
    console.log("  Use --import flag to actually write data.");
    process.exit(1);
}

const filePath = args[0];
const isImport = args.includes('--import');
const isDryRun = !isImport;

let admin;
let db;
let hasRealCredentials = false;

try {
    admin = require('firebase-admin');
    
    // Check for GOOGLE_APPLICATION_CREDENTIALS environment variable
    if (process.env.GOOGLE_APPLICATION_CREDENTIALS && fs.existsSync(process.env.GOOGLE_APPLICATION_CREDENTIALS)) {
        admin.initializeApp();
        hasRealCredentials = true;
    } 
    // Fallback to local serviceAccountKey.json
    else if (fs.existsSync('./serviceAccountKey.json')) {
        const serviceAccount = require('./serviceAccountKey.json');
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        });
        hasRealCredentials = true;
    } else {
        throw new Error("No credentials found");
    }
    db = admin.firestore();
} catch (e) {
    if (isImport) {
        console.error("\n\u274C REAL FIRESTORE IMPORT REQUIRES FIREBASE ADMIN CREDENTIALS");
        console.error("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable or provide scripts/serviceAccountKey.json");
        process.exit(1);
    } else {
        console.log("\u26A0\uFE0F Warning: Firebase credentials not found. Running DRY RUN with MOCK Firestore for existing data validation.");
        // Mock db for testing existing validation locally without credentials
        db = {
            collection: (name) => ({
                get: async () => ({ docs: [] })
            })
        };
    }
}

// Helper to remove internal fields starting with '_'
function sanitizeData(obj) {
    const sanitized = {};
    for (const key in obj) {
        if (!key.startsWith('_')) {
            sanitized[key] = obj[key];
        }
    }
    return sanitized;
}

async function runImport(filePath) {
    console.log(`\n=== Starting ${isDryRun ? 'DRY RUN' : 'IMPORT'} ===`);
    
    if (!fs.existsSync(filePath)) {
        console.error(`Error: File ${filePath} not found.`);
        process.exit(1);
    }

    const rawData = fs.readFileSync(filePath, 'utf-8');
    let data;
    try {
        data = JSON.parse(rawData);
    } catch (e) {
        console.error("Error: Invalid JSON format.");
        process.exit(1);
    }

    const crops = data.crops || [];
    const problems = data.agricultural_problems || [];
    const products = data.products || [];

    console.log(`Found: ${crops.length} crops, ${problems.length} problems, ${products.length} products.`);

    // 1. Validation: Required fields and Types
    let hasErrors = false;
    
    crops.forEach((c, i) => {
        if (!c.id || typeof c.id !== 'string') { console.error(`Crop at index ${i} is missing a valid 'id'.`); hasErrors = true; }
        if (!c.name) { console.error(`Crop ${c.id || i} is missing 'name'.`); hasErrors = true; }
    });

    problems.forEach((p, i) => {
        if (!p.id || typeof p.id !== 'string') { console.error(`Problem at index ${i} is missing a valid 'id'.`); hasErrors = true; }
        if (!p.cropId) { console.error(`Problem ${p.id || i} is missing 'cropId'.`); hasErrors = true; }
        if (!p.name) { console.error(`Problem ${p.id || i} is missing 'name'.`); hasErrors = true; }
        const validTypes = ['disease', 'pest', 'nutrient_deficiency', 'irrigation_problem', 'soil_problem', 'other'];
        if (!validTypes.includes(p.type)) {
            console.error(`Problem ${p.id} has invalid type '${p.type}'. Must be one of: ${validTypes.join(', ')}`);
            hasErrors = true;
        }
    });

    products.forEach((p, i) => {
        if (!p.id || typeof p.id !== 'string') { console.error(`Product at index ${i} is missing a valid 'id'.`); hasErrors = true; }
        if (!p.name) { console.error(`Product ${p.id || i} is missing 'name'.`); hasErrors = true; }
    });

    // 2. Validation: Duplicate IDs in JSON
    const getDuplicates = (arr) => {
        const ids = arr.map(x => x.id);
        return ids.filter((item, index) => ids.indexOf(item) !== index);
    };
    
    const dupCrops = getDuplicates(crops);
    const dupProblems = getDuplicates(problems);
    const dupProducts = getDuplicates(products);

    if (dupCrops.length > 0) { console.error(`Duplicate Crop IDs found: ${dupCrops.join(', ')}`); hasErrors = true; }
    if (dupProblems.length > 0) { console.error(`Duplicate Problem IDs found: ${dupProblems.join(', ')}`); hasErrors = true; }
    if (dupProducts.length > 0) { console.error(`Duplicate Product IDs found: ${dupProducts.join(', ')}`); hasErrors = true; }

    // 3. Validation: Relational Integrity (Foreign Keys)
    const jsonCropIds = new Set(crops.map(c => c.id));
    const jsonProductIds = new Set(products.map(p => p.id));

    // Fetch existing IDs from Firestore to allow linking to existing records
    let existingCropIds = new Set();
    let existingProductIds = new Set();
    
    try {
        const existingCropsSnap = await db.collection('crops').get();
        existingCropsSnap.docs.forEach(doc => existingCropIds.add(doc.id));
        
        const existingProductsSnap = await db.collection('products').get();
        existingProductsSnap.docs.forEach(doc => existingProductIds.add(doc.id));
    } catch (e) {
        console.error("Warning: Could not fetch existing data from Firestore for validation.", e.message);
    }

    const allValidCropIds = new Set([...jsonCropIds, ...existingCropIds]);
    const allValidProductIds = new Set([...jsonProductIds, ...existingProductIds]);

    problems.forEach(p => {
        if (!allValidCropIds.has(p.cropId)) {
            console.error(`Relational Error: Problem '${p.id}' references unknown cropId '${p.cropId}'.`);
            hasErrors = true;
        }
        if (p.recommendedProductIds && Array.isArray(p.recommendedProductIds)) {
            p.recommendedProductIds.forEach(prodId => {
                if (!allValidProductIds.has(prodId)) {
                    console.error(`Relational Error: Problem '${p.id}' references unknown recommendedProductId '${prodId}'.`);
                    hasErrors = true;
                }
            });
        }
    });

    if (hasErrors) {
        console.error("\n\u274C Validation Failed. Please fix the errors in your JSON file and try again.");
        process.exit(1);
    } else {
        console.log("\u2705 Validation Passed! Schema and relationships are valid.");
    }

    if (isDryRun) {
        console.log("DRY RUN completed successfully. No data was written to Firestore.");
        process.exit(0);
    }

    console.log("Writing data to Firestore...");
    try {
        const batch = db.batch();
        
        // Use Set with merge: true to avoid overwriting existing data blindly or creating duplicates.
        // Sanitize data to remove internal fields starting with '_'
        crops.forEach(c => {
            batch.set(db.collection('crops').doc(c.id), sanitizeData(c), { merge: true });
        });
        problems.forEach(p => {
            batch.set(db.collection('agricultural_problems').doc(p.id), sanitizeData(p), { merge: true });
        });
        products.forEach(p => {
            batch.set(db.collection('products').doc(p.id), sanitizeData(p), { merge: true });
        });

        await batch.commit();
        console.log("\u2705 IMPORT SUCCESSFUL. All data has been written to Firestore.");
    } catch (e) {
        console.error("\u274C Failed to write to Firestore:", e);
        process.exit(1);
    }
}

runImport(filePath);
