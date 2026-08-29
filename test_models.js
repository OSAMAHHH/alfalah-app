require('dotenv').config({path: 'backend/.env'});
const { GoogleGenAI } = require('@google/genai');

async function testModel(modelName) {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
    const start = Date.now();
    const response = await ai.models.generateContent({
      model: modelName,
      contents: "ما هو أفضل سماد للطماطم؟ أجب بجملة واحدة.",
    });
    const elapsed = Date.now() - start;
    console.log(`[SUCCESS] ${modelName} - Time: ${elapsed}ms - Response: ${response.text}`);
  } catch (e) {
    console.log(`[ERROR] ${modelName} - Status: ${e.status || 'N/A'} - Message: ${e.message}`);
  }
}

async function runAll() {
  await testModel('gemini-3.7-flash');
  await testModel('gemini-3.6-flash');
  await testModel('gemini-3.5-flash-lite');
}

runAll();
