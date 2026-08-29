require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');
async function run() {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
    const response = await ai.models.generateContent({
      model: 'gemini-1.5-flash',
      contents: "hello",
    });
    console.log("Response:", response.text);
  } catch (e) {
    console.error("Error Status:", e.status);
    console.error("Error Message:", e.message);
  }
}
run();
