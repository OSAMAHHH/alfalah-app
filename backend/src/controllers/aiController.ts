import { Response } from 'express';
import { AuthenticatedRequest } from '../middleware/authMiddleware';
import * as aiService from '../services/aiService';

export const handleChat = async (req: AuthenticatedRequest, res: Response) => {
  try {
    const { message, conversationId } = req.body;

    // Validate the input message
    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      return res.status(400).json({ error: 'Message is required and must be a valid string.' });
    }

    // Basic length limit for safety (e.g. 1000 characters)
    if (message.length > 1000) {
      return res.status(400).json({ error: 'Message exceeds the maximum allowed length of 1000 characters.' });
    }

    // Process chat using the AI service abstraction
    const response = await aiService.processChat({ message, conversationId });
    
    return res.json(response);
  } catch (error: any) {
    console.error('Error in handleChat:', error?.message || error);
    
    // Check if it's our custom AiServiceError
    if (error && error.status) {
      const statusCode = (error.status === 404 || error.status === 403) ? 500 : error.status;
      return res.status(statusCode).json({ error: error.message });
    }
    
    // Fallback for unexpected errors
    return res.status(500).json({ error: 'حدث خطأ داخلي في الخادم.' });
  }
};
