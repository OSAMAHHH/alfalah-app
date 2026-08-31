import * as fs from 'fs';
import { db } from './src/config/firebase';

async function validate() {
  if (!db) {
    console.error("No DB connection");
    process.exit(1);
  }

  const batch2Raw = fs.readFileSync('../scripts/batch_2_verified.json', 'utf8');
  const batch2 = JSON.parse(batch2Raw);
  const problems = batch2.agricultural_problems || [];

  console.log(`TOTAL_PROBLEMS:${problems.length}`);

  // Get existing problem IDs
  const problemsSnap = await db.collection('agricultural_problems').get();
  const existingProblemIds = new Set(problemsSnap.docs.map(d => d.id));
  console.log(`EXISTING_PROBLEMS:${existingProblemIds.size}`);

  // Get existing crop IDs
  const cropsSnap = await db.collection('crops').get();
  const existingCropIds = new Set(cropsSnap.docs.map(d => d.id));
  console.log(`EXISTING_CROPS:${existingCropIds.size}`);

  // Get existing product IDs
  const productsSnap = await db.collection('products').get();
  const existingProductIds = new Set(productsSnap.docs.map(d => d.id));
  console.log(`EXISTING_PRODUCTS:${existingProductIds.size}`);

  let duplicateIds = 0;
  let newIds = 0;
  let validCrops = 0;
  let invalidCrops = 0;
  let invalidProducts = 0;

  for (const p of problems) {
    if (existingProblemIds.has(p.id)) {
      duplicateIds++;
    } else {
      newIds++;
    }

    if (existingCropIds.has(p.cropId)) {
      validCrops++;
    } else {
      invalidCrops++;
      console.log(`INVALID_CROP:${p.cropId} for problem ${p.id}`);
    }

    if (p.recommendedProductIds && Array.isArray(p.recommendedProductIds)) {
      for (const prodId of p.recommendedProductIds) {
        if (!existingProductIds.has(prodId)) {
          invalidProducts++;
          console.log(`INVALID_PRODUCT:${prodId} for problem ${p.id}`);
        }
      }
    }
  }

  console.log(`DUPLICATE_IDS:${duplicateIds}`);
  console.log(`NEW_IDS:${newIds}`);
  console.log(`VALID_CROPS:${validCrops}`);
  console.log(`INVALID_CROPS:${invalidCrops}`);
  console.log(`INVALID_PRODUCTS:${invalidProducts}`);
  
  if (duplicateIds === 0 && invalidCrops === 0 && invalidProducts === 0) {
    console.log("VALIDATION_PASS");
  } else {
    console.log("VALIDATION_FAIL");
  }
}

validate().catch(console.error);
