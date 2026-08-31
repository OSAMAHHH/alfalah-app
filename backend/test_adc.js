const { initializeApp, applicationDefault } = require('firebase-admin/app');
const { getFirestore } = require('firebase-admin/firestore');

initializeApp({
  credential: applicationDefault(),
  projectId: 'alfalah-90856'
});

const db = getFirestore();
db.collection('agricultural_problems').limit(1).get().then(snap => {
  console.log("ADC Success! Found", snap.size);
}).catch(err => {
  console.error("ADC Failed:", err.message);
});
