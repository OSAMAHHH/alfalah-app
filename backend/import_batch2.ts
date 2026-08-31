import * as fs from 'fs';
import { db } from './src/config/firebase';

async function importData() {
  if (!db) {
    console.error("No DB connection");
    process.exit(1);
  }

  const batch2Raw = fs.readFileSync('../scripts/batch_2_verified.json', 'utf8');
  const batch2 = JSON.parse(batch2Raw);
  const problems = batch2.agricultural_problems || [];

  console.log(`Starting import of ${problems.length} problems...`);

  const batch = db.batch();

  for (const p of problems) {
    const docId = p.id;
    const cleanData: any = {};
    
    // Copy all keys
    for (const key of Object.keys(p)) {
      // Rule 7: Remove fields starting with _
      // Rule 8: Do not write "id" field inside document
      if (!key.startsWith('_') && key !== 'id') {
        cleanData[key] = p[key];
      }
    }

    // Set doc using Document ID
    const docRef = db.collection('agricultural_problems').doc(docId);
    batch.set(docRef, cleanData, { merge: true });
  }

  await batch.commit();
  console.log("Import committed successfully.");
}

importData().catch(console.error);
