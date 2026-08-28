const { GoogleGenAI } = require('@google/genai');
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
async function test() {
  try {
    const res = await ai.models.generateContent({ model: 'gemini-3.7-flash', contents: 'hi' });
    console.log("3.7 SUCCESS:", res.text);
  } catch (e) {
    console.error("3.7 ERROR:", e.message);
  }
}
test();
