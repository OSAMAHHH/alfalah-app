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
  const { message, history } = request;
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    throw new AiServiceError("عذراً، مفتاح GEMINI_API_KEY غير متوفر في الخادم.", 500);
  }
  const ai = new GoogleGenAI({ apiKey });

  // 1. History-aware & Multi-factor Query Analysis
  const analysis = await analyzeQuery(message, history);
  const { intent, matchedCrop, matches, confidence } = analysis;

  let systemContext = "";
  let finalRecommendedProductIds: string[] = [];
  let source: "KNOWLEDGE_BASE" | "GEMINI_WITH_KNOWLEDGE" | "GEMINI_GENERAL" = "GEMINI_GENERAL";

  // 2. Build Context based on local analysis & confidence level
  if (intent === "GENERAL") {
    source = "GEMINI_GENERAL";
    systemContext = `
      أنت المساعد الذكي لتطبيق 'الفلاح'.
      سؤال المستخدم غير زراعي. أجب على سؤاله بشكل طبيعي، مهذب، ومباشر دون إطالة.
    `;
  } else {
    // Intent is AGRICULTURAL
    if (confidence === "HIGH" || (confidence === "MEDIUM" && matches.length > 0)) {
      const topMatch = matches[0];
      const topMatches = matches.slice(0, 2);
      
      // Determine source precision
      if (topMatch.score >= 70) {
        source = "KNOWLEDGE_BASE";
      } else {
        source = "GEMINI_WITH_KNOWLEDGE";
      }

      // Collect recommended products
      const productIds = new Set<string>();
      topMatches.forEach(m => {
        if (m.problem.recommendedProductIds) {
          m.problem.recommendedProductIds.forEach(id => productIds.add(id));
        }
      });

      const products = await getActiveProductsByIds(Array.from(productIds));
      finalRecommendedProductIds = products.map((p: any) => p.id);

      const targetCropName = (matchedCrop ? matchedCrop.name : topMatch.matchedCrop?.name) || "المحصول";

      systemContext = `
        أنت المساعد الزراعي الذكي لتطبيق 'الفلاح'، تتحدث مع مزارع يمني بلغة عربية بسيطة، واضحة ومباشرة.
        
        تم العثور على تشخيص مطابق في قاعدة معرفة 'الفلاح' المعتمدة:
        - المحصول: ${targetCropName}
        ${topMatches.map(m => `
        - اسم المشكلة/الآفة: ${m.problem.name} (نوعها: ${m.problem.type})
          الأعراض: ${m.problem.symptoms ? m.problem.symptoms.join('، ') : 'غير محددة'}
          الأسباب: ${m.problem.causes || 'عوامل بيئية/حشرية/فطرية'}
          طريقة العلاج المعتمدة: ${m.problem.treatment || 'اتباع الرش الوقائي'}
          طرق الوقاية: ${m.problem.prevention || 'العناية بالري والتهوية'}
        `).join('\n')}

        المنتجات المتوفرة للعلاج في متجر الفلاح:
        ${products.length > 0 ? products.map(p => `- ${p.name}: ${p.usage} (الجرعة: ${p.dosage || 'حسب الملصق'})`).join('\n') : 'لا يوجد منتج تجاري مسجل حالياً في المتجر لهذه المشكلة المحددة.'}

        قواعد الإجابة الصارمة:
        1. ابدأ فوراً بدون مقدمات إنشائية أو ترحيب طويل.
        2. هيكل إجابتك كالتالي:
           - التشخيص الأرجح: اذكر اسم المشكلة (${topMatch.problem.name}) مباشرة.
           - الأعراض والمسببات باختصار شديد.
           - خطة العلاج المعتمدة من الدليل: اذكر العلاج والمنتجات المتوفرة بالاسم إن وجدت، أو وضح المادة الفعالة/الإجراء الزراعي إذا لم يتوفر منتج بالمتجر.
           - نصيحة وقائية سريعة للمستقبل.
        3. منع الهلوسة: لا تخترع أسماء مبيدات أو أسمدة أو شركات تجارية من خارج القائمة أعلاه مطلقاً.
        4. لا تذكر أي أرقام تقييم (Scores) أو مصطلحات برمجية.
      `;
    } else {
      // AGRICULTURAL but no reliable match in knowledge base (Score < 35 or no match)
      source = "GEMINI_GENERAL";
      const cropName = matchedCrop ? matchedCrop.name : "الزرع/المحصول";

      systemContext = `
        أنت المساعد الزراعي الذكي لتطبيق 'الفلاح'.
        يسأل المستخدم عن مشكلة أو استفسار زراعي يخص (${cropName}).
        
        تنبيه هام: هذه الحالة غير مسجلة في قاعدة معرفة أو دليل 'الفلاح' حالياً.
        
        التعليمات لك:
        1. أجب بأسلوب خبير زراعي ناصح ومفيد للمزارع اليمني.
        2. ابدأ مباشرة بالاحتمال الزراعي العلمي الأرجح ثم الأعراض والنصائح المتبعة.
        3. اذكر بوضوح وبكل أمانة أن هذه إرشادات زراعية عامة لعدم توفر تسجيل لهذه الحالة في دليل الفلاح حالياً.
        4. تحذير حاسم ضد الهلوسة: يُمنع منعاً باتاً اختراع أي أسماء تجارية لمنتجات أو مبيدات أو أسمدة محددة. اكتفِ بالاسم العلمي أو المادة الفعالة أو المعاملات الزراعية والوقائية (كالري، التقليم، أو المكافحة العضوية).
      `;
    }
  }

  // 3. Format history for memory
  let historyText = "";
  if (history && history.length > 0) {
    historyText = "سياق المحادثة السابقة بينك وبين المزارع:\n" + 
      history.map(h => `${h.role === 'user' ? 'المزارع' : 'المساعد'}: ${h.content}`).join("\n") + "\n\n";
  }

  const finalPrompt = `
    التوجيهات والسياق:
    ${systemContext}
    
    ${historyText}
    رسالة المزارع الحالية: "${message}"
  `;

  // Standard and fast Gemini model
  const finalResponse = await generateWithRetry(ai, 'gemini-3.6-flash', finalPrompt);

  return {
    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds,
    source
  };
};
