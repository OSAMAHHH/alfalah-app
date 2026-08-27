import { processChat } from './src/services/aiService';
import dotenv from 'dotenv';
dotenv.config();

async function run() {
  try {
    console.log("Testing Gemini API directly...");
    const res = await processChat({ message: "ما سبب اصفرار أوراق الطماطم؟", conversationId: "123" });
    console.log("Response:", res.answer);
  } catch (e) {
    console.error("Error:", e);
  }
}
run();
