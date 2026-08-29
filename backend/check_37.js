const { GoogleGenAI } = require('@google/genai');

async function test(modelName) {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
    const response = await ai.models.generateContent({
      model: modelName,
      contents: "Hi",
      config: { maxOutputTokens: 5 }
    });
    console.log(`[OK] ${modelName} responded`);
  } catch(e) {
    console.log(`[ERR] ${modelName}: ${e.status} ${e.message}`);
  }
}

test('gemini-3.7-flash');
setTimeout(() => { console.log('Timeout reached'); process.exit(1); }, 4000);
