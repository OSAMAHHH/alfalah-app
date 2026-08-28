const fs = require('fs');
const path = './backend/src/services/aiService.ts';

const newCode = `import { AiChatRequest, AiChatResponse } from '../types';
import { GoogleGenAI } from '@google/genai';
import { matchProblem, getActiveProductsByIds } from './knowledgeBaseService';

export class AiServiceError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

// Helper to delay execution
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

// Helper to wrap Gemini calls with retry logic
const generateWithRetry = async (ai: GoogleGenAI, model: string, contents: string, maxRetries = 3): Promise<any> => {
  let attempt = 0;
  while (attempt <= maxRetries) {
    try {
      return await ai.models.generateContent({ model, contents });
    } catch (error: any) {
      console.error(\`Gemini API Error (Attempt \${attempt + 1}):\`, error?.message || error);
      
      const status = error?.status || (error?.message?.includes('429') ? 429 : 
                                      (error?.message?.includes('503') || error?.message?.includes('high demand') || error?.message?.includes('UNAVAILABLE') ? 503 : 500));
      
      // If it's a rate limit (429) or service unavailable (503), retry
      if ((status === 429 || status === 503) && attempt < maxRetries) {
        attempt++;
        const backoffTime = Math.pow(2, attempt) * 1000 + Math.random() * 1000; // Exponential backoff with jitter
        console.log(\`Retrying in \${Math.round(backoffTime)}ms...\`);
        await delay(backoffTime);
        continue;
      }
      
      // Throw appropriate error if out of retries or it's a non-retriable error
      if (status === 429) {
        throw new AiServiceError("تجاوزت حد الاستخدام أو يوجد ضغط كبير. يرجى المحاولة بعد قليل.", 429);
      } else if (status === 503) {
        throw new AiServiceError("خوادم الذكاء الاصطناعي غير متاحة مؤقتاً. يرجى المحاولة لاحقاً.", 503);
      } else {
        throw new AiServiceError("حدث خطأ أثناء التواصل مع خوادم الذكاء الاصطناعي.", 500);
      }
    }
  }
};

/**
 * Service abstraction for Gemini Integration with RAG (Retrieval-Augmented Generation).
 */
export const processChat = async (request: AiChatRequest): Promise<AiChatResponse> => {
  const apiKey = process.env.GEMINI_API_KEY;
  
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    throw new AiServiceError("عذراً، مفتاح GEMINI_API_KEY غير متوفر في الخادم.", 500);
  }

  const ai = new GoogleGenAI({ apiKey });
  
  // Step 1: Entity Extraction
  const extractionPrompt = \`
    قم بتحليل استفسار المستخدم الزراعي التالي بدقة.
    استخرج المعلومات التالية وأعدها بصيغة JSON فقط بدون أي نصوص إضافية أو Markdown:
    {
      "cropName": "اسم المحصول، أو null إذا لم يذكر",
      "symptoms": ["العرض الأول", "العرض الثاني"],
      "problemType": "نوع المشكلة مثل حشرة، مرض، نقص عناصر، أو null إذا لم يذكر"
    }
    استفسار المستخدم: "\${request.message}"
  \`;

  const extractionResponse = await generateWithRetry(ai, 'gemini-3.6-flash', extractionPrompt);
  
  let extractedData = { cropName: null, symptoms: [], problemType: null };
  try {
    const rawText = extractionResponse.text?.replace(/\\x60\\x60\\x60json/g, '').replace(/\\x60\\x60\\x60/g, '').trim() || '{}';
    extractedData = JSON.parse(rawText);
  } catch (e) {
    console.warn("Failed to parse Gemini extraction JSON", e);
  }

  // Step 2: Matching Engine
  const { matches, matchedCrop } = await matchProblem(
    extractedData.cropName, 
    extractedData.symptoms, 
    extractedData.problemType
  );

  let systemContext = "";
  let finalRecommendedProductIds: string[] = [];

  // Step 3: Context Assembly based on Matching Scores
  if (!matchedCrop) {
    systemContext = \`المستخدم يسأل سؤالاً زراعياً ولكن لم نتمكن من تحديد المحصول في قاعدة بياناتنا. 
    اعتذر بلطف، واطلب منه توضيح اسم المحصول أو التأكد من إضافته، وتوضيح الأعراض. لا تقترح حلولاً من خارج النظام.\`;
  } else if (matches.length > 0) {
    const topMatch = matches[0];
    
    if (topMatch.score >= 70) {
      // High confidence
      const products = await getActiveProductsByIds(topMatch.problem.recommendedProductIds || []);
      finalRecommendedProductIds = products.map(p => p.id);
      
      systemContext = \`
        أنت مساعد زراعي خبير وموثوق في تطبيق 'الفلاح'.
        تحدث بثقة وود.
        بناءً على قاعدة المعرفة الخاصة بنا، المشكلة الأقرب بنسبة مطابقة عالية لمحصول (\${matchedCrop.name}) هي: (\${topMatch.problem.name}).
        الأسباب: \${topMatch.problem.causes}
        طرق العلاج: \${topMatch.problem.treatment}
        المنتجات المتوفرة للعلاج في نظامنا: \${products.map(p => p.name + ' - ' + p.usage).join(', ')}
        
        التعليمات لك:
        - صغ إجابة تفصيلية ومطمئنة للمستخدم توضح المشكلة والحلول.
        - اذكر المنتجات المرفقة فقط كحل مقترح (إذا توفرت). لا تخترع أو تقترح منتجات من خارج النظام أبداً.
        - لا تذكر النقاط (Scores) للمستخدم.
      \`;
    } else if (topMatch.score >= 40) {
      // Low confidence
      systemContext = \`
        أنت مساعد زراعي في تطبيق 'الفلاح'.
        المستخدم يواجه مشكلة في محصول (\${matchedCrop.name}). 
        الأعراض المذكورة تتشابه جزئياً مع المشكلة: (\${topMatch.problem.name}).
        
        التعليمات لك:
        - لا تقم بتشخيص قاطع. استخدم عبارات مثل "قد تتوافق الأعراض مع..." أو "يُحتمل أن تكون...".
        - اذكر أن المعلومات غير كافية لتشخيص دقيق واطلب منه توضيح أعراض إضافية.
        - لا تقترح منتجات في هذه المرحلة.
      \`;
    } else {
      // Unsure
      systemContext = \`
        أنت مساعد زراعي في تطبيق 'الفلاح'.
        المحصول المذكور هو (\${matchedCrop.name}) ولكن الأعراض لا تتطابق مع أي مشكلة معروفة في قاعدة بياناتنا.
        التعليمات لك:
        - اعتذر بلطف.
        - اطلب من المستخدم وصف المشكلة بشكل أدق وأكثر تفصيلاً لنتمكن من مساعدته.
        - لا تقترح حلولاً من خارج النظام.
      \`;
    }
  } else {
    systemContext = \`المحصول (\${matchedCrop.name}) موجود لدينا ولكن لا توجد مشاكل زراعية مسجلة له حالياً. اطلب منه مراجعة المهندس الزراعي المختص أو انتظار تحديثات الإدارة.\`;
  }

  // Step 4: Final Generation (RAG)
  const finalPrompt = \`
    السياق والمعلومات الموثوقة (لا تتجاوزها):
    \${systemContext}
    
    سؤال المستخدم: "\${request.message}"
  \`;

  const finalResponse = await generateWithRetry(ai, 'gemini-3.6-flash', finalPrompt);

  return {
    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds
  };
};
`;

fs.writeFileSync(path, newCode);
