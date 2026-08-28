import { AiChatRequest, AiChatResponse } from '../types';
import { GoogleGenAI } from '@google/genai';
import { matchProblem, getActiveProductsByIds } from './knowledgeBaseService';

/**
 * Service abstraction for Gemini Integration with RAG (Retrieval-Augmented Generation).
 */
export const processChat = async (request: AiChatRequest): Promise<AiChatResponse> => {
  const apiKey = process.env.GEMINI_API_KEY;
  
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    return {
      answer: "عذراً، مفتاح GEMINI_API_KEY غير متوفر في الخادم. يرجى إعداده لكي يعمل المساعد الذكي.",
      recommendedProducts: []
    };
  }

  try {
    const ai = new GoogleGenAI({ apiKey });
    
    // Step 1: Entity Extraction
    const extractionPrompt = `
      قم بتحليل استفسار المستخدم الزراعي التالي بدقة.
      استخرج المعلومات التالية وأعدها بصيغة JSON فقط بدون أي نصوص إضافية أو Markdown:
      {
        "cropName": "اسم المحصول، أو null إذا لم يذكر",
        "symptoms": ["العرض الأول", "العرض الثاني"],
        "problemType": "نوع المشكلة مثل حشرة، مرض، نقص عناصر، أو null إذا لم يذكر"
      }
      استفسار المستخدم: "${request.message}"
    `;

    const extractionResponse = await ai.models.generateContent({
      model: 'gemini-3.6-flash',
      contents: extractionPrompt,
    });
    
    let extractedData = { cropName: null, symptoms: [], problemType: null };
    try {
      const rawText = extractionResponse.text?.replace(/```json/g, '').replace(/```/g, '').trim() || '{}';
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
      systemContext = `المستخدم يسأل سؤالاً زراعياً ولكن لم نتمكن من تحديد المحصول في قاعدة بياناتنا. 
      اعتذر بلطف، واطلب منه توضيح اسم المحصول أو التأكد من إضافته، وتوضيح الأعراض. لا تقترح حلولاً من خارج النظام.`;
    } else if (matches.length > 0) {
      const topMatch = matches[0];
      
      if (topMatch.score >= 70) {
        // High confidence
        const products = await getActiveProductsByIds(topMatch.problem.recommendedProductIds || []);
        finalRecommendedProductIds = products.map(p => p.id);
        
        systemContext = `
          أنت مساعد زراعي خبير وموثوق في تطبيق 'الفلاح'.
          تحدث بثقة وود.
          بناءً على قاعدة المعرفة الخاصة بنا، المشكلة الأقرب بنسبة مطابقة عالية لمحصول (${matchedCrop.name}) هي: (${topMatch.problem.name}).
          الأسباب: ${topMatch.problem.causes}
          طرق العلاج: ${topMatch.problem.treatment}
          المنتجات المتوفرة للعلاج في نظامنا: ${products.map(p => p.name + ' - ' + p.usage).join(', ')}
          
          التعليمات لك:
          - صغ إجابة تفصيلية ومطمئنة للمستخدم توضح المشكلة والحلول.
          - اذكر المنتجات المرفقة فقط كحل مقترح (إذا توفرت). لا تخترع أو تقترح منتجات من خارج النظام أبداً.
          - لا تذكر النقاط (Scores) للمستخدم.
        `;
      } else if (topMatch.score >= 40) {
        // Low confidence
        systemContext = `
          أنت مساعد زراعي في تطبيق 'الفلاح'.
          المستخدم يواجه مشكلة في محصول (${matchedCrop.name}). 
          الأعراض المذكورة تتشابه جزئياً مع المشكلة: (${topMatch.problem.name}).
          
          التعليمات لك:
          - لا تقم بتشخيص قاطع. استخدم عبارات مثل "قد تتوافق الأعراض مع..." أو "يُحتمل أن تكون...".
          - اذكر أن المعلومات غير كافية لتشخيص دقيق واطلب منه توضيح أعراض إضافية.
          - لا تقترح منتجات في هذه المرحلة.
        `;
      } else {
        // Unsure
        systemContext = `
          أنت مساعد زراعي في تطبيق 'الفلاح'.
          المحصول المذكور هو (${matchedCrop.name}) ولكن الأعراض لا تتطابق مع أي مشكلة معروفة في قاعدة بياناتنا.
          التعليمات لك:
          - اعتذر بلطف.
          - اطلب من المستخدم وصف المشكلة بشكل أدق وأكثر تفصيلاً لنتمكن من مساعدته.
          - لا تقترح حلولاً من خارج النظام.
        `;
      }
    } else {
      systemContext = `المحصول (${matchedCrop.name}) موجود لدينا ولكن لا توجد مشاكل زراعية مسجلة له حالياً. اطلب منه مراجعة المهندس الزراعي المختص أو انتظار تحديثات الإدارة.`;
    }

    // Step 4: Final Generation (RAG)
    const finalPrompt = `
      السياق والمعلومات الموثوقة (لا تتجاوزها):
      ${systemContext}
      
      سؤال المستخدم: "${request.message}"
    `;

    const finalResponse = await ai.models.generateContent({
      model: 'gemini-3.6-flash',
      contents: finalPrompt,
    });

    return {
      answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
      recommendedProducts: finalRecommendedProductIds
    };
    
  } catch (error: any) {
    console.error('Error calling Gemini API:', error);
    throw new Error('Failed to communicate with Gemini API');
  }
};
