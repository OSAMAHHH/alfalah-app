const fs = require('fs');
const path = './backend/src/services/aiService.ts';
let code = fs.readFileSync(path, 'utf8');
code = code.replace(/throw new Error\('Failed to communicate with Gemini API'\);/g, `let errorMessage = "عذراً، المساعد الذكي غير قادر على معالجة طلبك حالياً.";
    if (error?.message?.includes('high demand') || error?.status === 503 || error?.status === 'UNAVAILABLE') {
      errorMessage = "عذراً، خوادم جوجل الذكية (Gemini) تواجه ضغطاً كبيراً في الوقت الحالي. يرجى المحاولة بعد قليل.";
    }
    return {
      answer: errorMessage,
      recommendedProducts: []
    };`);
fs.writeFileSync(path, code);
