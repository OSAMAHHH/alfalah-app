import { AiChatRequest, AiChatResponse } from '../types';
import { GoogleGenAI } from '@google/genai';
import { matchProblem, getActiveProductsByIds } from './knowledgeBaseService';

export class AiServiceError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

const generateWithRetry = async (ai: GoogleGenAI, model: string, contents: string, maxRetries = 3): Promise<any> => {
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
        const backoffTime = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
        console.log(`Retrying in ${Math.round(backoffTime)}ms...`);
        await delay(backoffTime);
        continue;
      }
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

export const processChat = async (request: AiChatRequest): Promise<AiChatResponse> => {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    throw new AiServiceError("عذراً، مفتاح GEMINI_API_KEY غير متوفر في الخادم.", 500);
  }
  const ai = new GoogleGenAI({ apiKey });

  const extractionPrompt = `
    قم بتحليل استفسار المستخدم التالي بدقة وحدد نية المستخدم (Intent).
    إذا كان السؤال يتعلق بالزراعة، المحاصيل (بما فيها القات)، النباتات، أمراض النباتات، الآفات، الأسمدة، المبيدات أو المنتجات الزراعية، فالنية هي "AGRICULTURAL".
    إذا كان السؤال عاماً لا علاقة له بالزراعة (مثل أسئلة جغرافية، عامة، ترحيب مجرد لا يتعلق بالزراعة)، فالنية هي "GENERAL".

    استخرج المعلومات التالية وأعدها بصيغة JSON فقط بدون أي نصوص إضافية أو Markdown:
    {
      "intent": "AGRICULTURAL أو GENERAL",
      "cropName": "اسم المحصول (بما في ذلك القات)، أو null إذا لم يذكر",
      "symptoms": ["العرض الأول", "العرض الثاني"],
      "problemType": "نوع المشكلة مثل حشرة، مرض، نقص عناصر، أو null إذا لم يذكر"
    }
    
    استفسار المستخدم: "${request.message}"
  `;

  const extractionResponse = await generateWithRetry(ai, 'gemini-3.6-flash', extractionPrompt);
  
  let extractedData = { intent: "GENERAL", cropName: null, symptoms: [], problemType: null };
  try {
    const rawText = extractionResponse.text?.replace(/\x60\x60\x60json/g, '').replace(/\x60\x60\x60/g, '').trim() || '{}';
    extractedData = JSON.parse(rawText);
  } catch (e) {
    console.warn("Failed to parse Gemini extraction JSON", e);
  }

  if (extractedData.intent === "GENERAL") {
    // General chat, bypass RAG
    const generalPrompt = `
      أنت مساعد مفيد وذكي. أجب على سؤال المستخدم بشكل طبيعي وودي. 
      سؤال المستخدم: "${request.message}"
    `;
    const finalResponse = await generateWithRetry(ai, 'gemini-3.6-flash', generalPrompt);
    return {
      answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
      recommendedProducts: []
    };
  }

  // Intent is AGRICULTURAL
  let systemContext = "";
  let finalRecommendedProductIds: string[] = [];

  if (extractedData.cropName) {
    const { matches, matchedCrop } = await matchProblem(
      extractedData.cropName, 
      extractedData.symptoms, 
      extractedData.problemType
    );

    if (matchedCrop && matches.length > 0) {
      const topMatch = matches[0];
      if (topMatch.score >= 70) {
        // High confidence
        const products = await getActiveProductsByIds(topMatch.problem.recommendedProductIds || []);
        finalRecommendedProductIds = products.map((p: any) => p.id);
        
        systemContext = `
          أنت مساعد زراعي خبير وموثوق في تطبيق 'الفلاح'.
          بناءً على قاعدة المعرفة الخاصة بنا، المشكلة الأقرب بنسبة مطابقة عالية لمحصول (${matchedCrop.name}) هي: (${topMatch.problem.name}).
          الأسباب: ${topMatch.problem.causes}
          طرق العلاج: ${topMatch.problem.treatment}
          المنتجات المتوفرة للعلاج في متجرنا: ${products.map((p: any) => p.name + ' - ' + p.usage).join(', ')}
          
          التعليمات لك:
          - صغ إجابة تفصيلية ومطمئنة للمستخدم توضح المشكلة والحلول بناء على هذه المعلومات فقط.
          - اذكر المنتجات المرفقة في سياق حديثك فقط كحل مقترح (إذا توفرت).
          - تحذير هام: لا تخترع أو تقترح أسماء منتجات، جرعات، أو معرفات من خارج النظام أبداً.
          - لا تذكر النقاط (Scores).
        `;
      } else if (topMatch.score >= 40) {
        // Low confidence
        systemContext = `
          أنت مساعد زراعي في تطبيق 'الفلاح'.
          المستخدم يواجه مشكلة في محصول (${matchedCrop.name}). الأعراض المذكورة تتشابه جزئياً مع المشكلة: (${topMatch.problem.name}).
          التعليمات:
          - لا تقم بتشخيص قاطع. استخدم عبارات مثل "قد تتوافق الأعراض مع..." 
          - يمكنك إضافة معلومات زراعية عامة صحيحة عن هذا المحصول.
          - تحذير هام: لا تخترع منتجات أو أدوية من خارج قاعدة المعرفة. لا تقترح منتجات في هذه المرحلة.
        `;
      } else {
        // Matched crop but no matching problem
        systemContext = `
          أنت مساعد زراعي خبير في تطبيق 'الفلاح'.
          المحصول المذكور هو (${matchedCrop.name}) (قد يكون القات أو أي محصول آخر). الأعراض لا تتطابق مع مشكلة معينة في قاعدة بياناتنا.
          التعليمات لك:
          - أجب بناءً على معرفتك الزراعية العامة وخبرتك كمستشار زراعي.
          - قدم نصائح زراعية مفيدة وصحيحة.
          - تحذير هام جداً: يُمنع منعاً باتاً اختراع أسماء منتجات زراعية تجارية أو مبيدات أو أسمدة محددة غير موجودة. اكتفِ بالنصائح العامة (مثل: استخدم سماد عضوي، تأكد من الري، الخ).
        `;
      }
    } else {
      // Crop mentioned but NOT found in our DB at all
      systemContext = `
        أنت مساعد زراعي خبير في تطبيق 'الفلاح'.
        المستخدم سأل عن محصول أو نبات (مثل: ${extractedData.cropName}) غير مسجل حالياً في قاعدة بياناتنا الخاصة بالمتجر.
        التعليمات لك:
        - لا تعتذر أو ترفض الإجابة. أجب على سؤاله أو استفساره الزراعي بناءً على خبرتك العامة.
        - قدم نصائح زراعية علمية وصحيحة.
        - تحذير هام جداً: يُمنع منعاً باتاً اقتراح أسماء منتجات تجارية أو مبيدات أو أسمدة محددة. اكتفِ بالأسماء العلمية أو النصائح والإجراءات العامة.
      `;
    }
  } else {
    // Agricultural question but NO specific crop mentioned (e.g. "ما هي أفضل طريقة للري؟" أو "ما فوائد هذا السماد؟")
    systemContext = `
      أنت مساعد زراعي خبير في تطبيق 'الفلاح'.
      يسأل المستخدم سؤالاً زراعياً عاماً لا يحدد فيه محصولاً معيناً.
      التعليمات لك:
      - أجب على سؤاله الزراعي بشكل مفيد وعلمي.
      - تحذير هام جداً: يُمنع اختراع أسماء منتجات تجارية.
    `;
  }

  const finalPrompt = `
    معلومات وتوجيهات لك (لا تذكرها للمستخدم مباشرة، بل نفذها):
    ${systemContext}
    
    سؤال المستخدم: "${request.message}"
  `;

  const finalResponse = await generateWithRetry(ai, 'gemini-3.6-flash', finalPrompt);
  
  return {
    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds
  };
};
