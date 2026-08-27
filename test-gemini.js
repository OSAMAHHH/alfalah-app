require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');

async function run() {
  try {
    console.log("Testing Gemini API directly with API KEY:", process.env.GEMINI_API_KEY ? "EXISTS" : "MISSING");
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
    const response = await ai.models.generateContent({
      model: 'gemini-3.7-flash',
      contents: "ما سبب اصفرار أوراق الطماطم؟ اجب باختصار.",
    });
    console.log("Response:", response.text);
  } catch (e) {
    console.error("Error:", e.message);
  }
}
run();
