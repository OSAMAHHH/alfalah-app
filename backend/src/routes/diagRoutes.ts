import { Router } from 'express';
import { db, auth } from '../config/firebase';
const router = Router();
router.get('/', (req, res) => {
  res.json({
    hasDb: !!db,
    hasAuth: !!auth,
    hasGeminiKey: !!process.env.GEMINI_API_KEY,
    geminiKeyLength: process.env.GEMINI_API_KEY ? process.env.GEMINI_API_KEY.length : 0,
    hasFirebaseCreds: !!process.env.FIREBASE_CREDENTIALS,
    firebaseCredsLength: process.env.FIREBASE_CREDENTIALS ? process.env.FIREBASE_CREDENTIALS.length : 0,
    firebaseCredsValidJson: (() => {
      try {
        JSON.parse(process.env.FIREBASE_CREDENTIALS || '{}');
        return true;
      } catch (e) {
        return false;
      }
    })()
  });
});
export default router;
