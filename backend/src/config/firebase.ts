import * as admin from 'firebase-admin';
import dotenv from 'dotenv';

dotenv.config();

// Initialize Firebase Admin
try {
  if (!admin.apps.length) {
    if (process.env.FIREBASE_CREDENTIALS) {
      // Used in production (e.g., Render) where the JSON is passed as an env string
      const serviceAccount = JSON.parse(process.env.FIREBASE_CREDENTIALS);
      admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
      });
      console.log('Firebase Admin initialized successfully via FIREBASE_CREDENTIALS.');
    } else {
      // Used locally, relies on GOOGLE_APPLICATION_CREDENTIALS env var
      admin.initializeApp();
      console.log('Firebase Admin initialized successfully via default local credentials.');
    }
  }
} catch (error) {
  console.error('Firebase Admin initialization error:', error);
}

export const db = admin.apps.length ? admin.firestore() : null;
export const auth = admin.apps.length ? admin.auth() : null;
