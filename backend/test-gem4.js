const { GoogleGenAI } = require('@google/genai');
async function run() {
  const ai = new GoogleGenAI({ apiKey: 'AIzaSyBKCAQCN_kmn4K8V2puqASWKsVMHU76i00' });
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-1.5-flash',
      contents: "hello",
    });
    console.log("Response 1.5:", response.text);
  } catch (e) {
    console.log("Error 1.5:", e.status, e.message);
  }
}
run();
