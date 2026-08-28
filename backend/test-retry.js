const { processChat } = require('./dist/services/aiService');
require('dotenv').config({ path: './backend/.env' });

// We can monkey patch GoogleGenAI to throw 503 for testing
const { GoogleGenAI } = require('@google/genai');
const originalGen = GoogleGenAI.prototype.models;

let attempts = 0;
// We'll mock the module by re-requiring and overriding, or simply override prototype
const testRetry = async () => {
    // Override the processChat if possible, wait, processChat uses GoogleGenAI instance.
    // It's easier to just run the backend and see it work.
    try {
        console.log("Testing actual processChat...");
        const res = await processChat({ message: "ما هي مشاكل الطماطم؟" });
        console.log("SUCCESS:", res.answer.substring(0, 50));
    } catch(e) {
        console.error("ERROR:", e);
    }
}
testRetry();
