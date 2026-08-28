const { GoogleGenAI } = require('@google/genai');
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
async function test() {
  try {
    const res = await ai.models.generateContent({ model: 'gemini-2.5-flash', contents: 'hi' });
    console.log("2.5 SUCCESS:", res.text);
  } catch (e) {
    console.error("2.5 ERROR:", e.message);
    try {
      const res2 = await ai.models.generateContent({ model: 'gemini-1.5-flash', contents: 'hi' });
      console.log("1.5 SUCCESS:", res2.text);
    } catch (e2) {
      console.error("1.5 ERROR:", e2.message);
    }
  }
}
test();
