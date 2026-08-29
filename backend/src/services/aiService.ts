import { AiChatRequest, AiChatResponse } from '../types';
import { GoogleGenAI } from '@google/genai';
import { analyzeQuery, getActiveProductsByIds } from './knowledgeBaseService';

export class AiServiceError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

const generateWithRetry = async (ai: GoogleGenAI, model: string, contents: string, maxRetries = 2): Promise<any> => {
  let attempt = 0;
  while (attempt <= maxRetries) {
    try {
      return await ai.models.generateContent({ model, contents });
    } catch (error: any) {
      console.error(`Gemini API Error (Attempt ${attempt + 1}):`, error?.message || error);
      const status = error?.status || (error?.message?.includes('429') ? 429 : 
                                       (error?.message?.includes('503') || error?.message?.includes('high demand') || error?.message?.includes('UNAVAILABLE') ? 503 : 500));
      if ((status === 429 || status === 503) && attempt < maxRetries) {
        attempt++;
        // Reduced backoff for faster response: 1s to 2s
        const backoffTime = 1000 + Math.random() * 1000;
        console.log(`Retrying in ${Math.round(backoffTime)}ms...`);
        await delay(backoffTime);
        continue;
      }
      
      let errorMessage = "عذراً، المساعد الذكي غير قادر على معالجة طلبك حالياً.";
      if (status === 429) {
        errorMessage = "تجاوزت حد الاستخدام أو يوجد ضغط كبير. يرجى المحاولة بعد قليل.";
      } else if (status === 503) {
        errorMessage = "خوادم الذكاء الاصطناعي تواجه ضغطاً كبيراً أو غير متاحة مؤقتاً. يرجى المحاولة لاحقاً.";
      }
      throw new AiServiceError(errorMessage, status);
    }
  }
};

export const processChat = async (request: AiChatRequest): Promise<AiChatResponse> => {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    throw new AiServiceError("عذراً، مفتاح GEMINI_API_KEY غير متوفر في الخادم.", 500);
  }
  const ai = new GoogleGenAI({ apiKey });

  // 1. Local Query Analysis (0 Gemini calls, cached Firestore)
  const { intent, matchedCrop, matches } = await analyzeQuery(request.message);

  let systemContext = "";
  let finalRecommendedProductIds: string[] = [];

  // 2. Build Context based on local analysis
  if (intent === "GENERAL") {
    systemContext = `
      أنت مساعد مفيد وذكي ومختصر. 
      هذا السؤال ليس زراعياً. أجب على سؤال المستخدم بشكل طبيعي وودي ومباشر.
    `;
  } else {
    // Intent is AGRICULTURAL
    if (matchedCrop) {
      if (matches.length > 0) {
        // Take top 2 matches to give Gemini context without overloading prompt
        const topMatches = matches.slice(0, 2);
        
        // Collect recommended products from top matches
        const productIds = new Set<string>();
        topMatches.forEach(m => {
          if (m.problem.recommendedProductIds) {
            m.problem.recommendedProductIds.forEach(id => productIds.add(id));
          }
        });
        
        const products = await getActiveProductsByIds(Array.from(productIds));
        finalRecommendedProductIds = products.map((p: any) => p.id);
        
        systemContext = `
          أنت مساعد زراعي خبير وموثوق في تطبيق 'الفلاح'.
          المحصول المذكور: (${matchedCrop.name}).
          بناءً على قاعدة المعرفة الخاصة بنا، إليك أبرز المشاكل الزراعية المطابقة لحالة المستخدم:
          ${topMatches.map(m => `- مشكلة: ${m.problem.name}\n  الأسباب: ${m.problem.causes}\n  العلاج: ${m.problem.treatment}`).join('\n\n')}
          
          المنتجات المتوفرة للعلاج في متجرنا: ${products.map((p: any) => p.name + ' - ' + p.usage).join(', ')}
          
          التعليمات لك:
          - اقرأ سؤال المستخدم وأعراضه بعناية، ثم استنتج المشكلة الأقرب من القائمة أعلاه.
          - صغ إجابة تفصيلية ومطمئنة للمستخدم توضح المشكلة والحلول.
          - اذكر المنتجات المرفقة في سياق حديثك فقط كحل مقترح (إذا توفرت).
          - تحذير هام جداً: لا تخترع أو تقترح أسماء منتجات، جرعات، أو أسمدة، أو مبيدات، أو معرفات من خارج النظام أبداً.
          - لا تذكر النقاط (Scores).
        `;
      } else {
        // Matched crop but no matching problem found
        systemContext = `
          أنت مساعد زراعي خبير في تطبيق 'الفلاح'.
          المحصول المذكور هو (${matchedCrop.name}) (قد يكون القات أو أي محصول آخر).
          التعليمات لك:
          - أجب بناءً على معرفتك الزراعية العامة وخبرتك كمستشار زراعي.
          - قدم نصائح زراعية مفيدة وصحيحة لهذا المحصول.
          - تحذير هام جداً: يُمنع منعاً باتاً اختراع أو اقتراح أسماء منتجات زراعية تجارية أو مبيدات أو أسمدة محددة غير موجودة في متجرنا. اكتفِ بالنصائح العامة أو المكونات الفعالة.
        `;
      }
    } else {
      // Agricultural question but NO specific crop matched
      systemContext = `
        أنت مساعد زراعي خبير في تطبيق 'الفلاح'.
        يسأل المستخدم سؤالاً زراعياً.
        التعليمات لك:
        - أجب على سؤاله الزراعي بشكل مفيد وعلمي.
        - قدم نصائح عامة مفيدة.
        - تحذير هام جداً: يُمنع منعاً باتاً اختراع أو اقتراح أسماء منتجات تجارية أو مبيدات أو أسمدة محددة غير موجودة في متجرنا. اكتفِ بالأسماء العلمية أو الإجراءات الزراعية.
      `;
    }
  }

  // 3. Single Gemini Call
  const finalPrompt = `
    معلومات وتوجيهات لك (لا تذكرها للمستخدم مباشرة، بل نفذها):
    ${systemContext}
    
    سؤال المستخدم: "${request.message}"
  `;

  // We use gemini-3.7-flash as it is the standard, fast, and supported model in the @google/genai SDK.
  const finalResponse = await generateWithRetry(ai, 'gemini-3.7-flash', finalPrompt);
  
  return {
    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds
  };
};
