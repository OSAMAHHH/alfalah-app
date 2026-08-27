import { Router } from 'express';
import { handleChat } from '../controllers/aiController';
import { verifyToken } from '../middleware/authMiddleware';

const router = Router();

// Endpoint for the AI assistant chat
// Protected by verifyToken middleware
router.post('/chat', verifyToken, handleChat);

export default router;
