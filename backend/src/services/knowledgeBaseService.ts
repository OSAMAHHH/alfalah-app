import { db } from '../config/firebase';
import { Crop, AgriculturalProblem, Product } from '../types';

// --- In-Memory Caches ---
let cropsCache: { data: Crop[], timestamp: number } | null = null;
let allProblemsCache: { data: AgriculturalProblem[], timestamp: number } | null = null;
let problemsCache: Record<string, { data: AgriculturalProblem[], timestamp: number }> = {};
let productsCache: Record<string, { data: Product, timestamp: number }> = {};

const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export const getActiveCrops = async (): Promise<Crop[]> => {
  if (!db) return [];
  if (cropsCache && Date.now() - cropsCache.timestamp < CACHE_TTL) {
    return cropsCache.data;
  }
  try {
    const snapshot = await db.collection('crops').where('isActive', '==', true).get();
    const results = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Crop));
    cropsCache = { data: results, timestamp: Date.now() };
    return results;
  } catch (error) {
    console.error('Error fetching crops:', error);
    return [];
  }
};

export const getActiveProblemsForCrop = async (cropId: string): Promise<AgriculturalProblem[]> => {
  if (!db) return [];
  if (problemsCache[cropId] && Date.now() - problemsCache[cropId].timestamp < CACHE_TTL) {
    return problemsCache[cropId].data;
  }
  try {
    const snapshot = await db.collection('agricultural_problems')
      .where('cropId', '==', cropId)
      .where('isActive', '==', true)
      .get();
    const results = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as AgriculturalProblem));
    problemsCache[cropId] = { data: results, timestamp: Date.now() };
    return results;
  } catch (error) {
    console.error('Error fetching problems for crop:', error);
    return [];
  }
};

export const getAllActiveProblems = async (): Promise<AgriculturalProblem[]> => {
  if (!db) return [];
  if (allProblemsCache && Date.now() - allProblemsCache.timestamp < CACHE_TTL) {
    return allProblemsCache.data;
  }
  try {
    const snapshot = await db.collection('agricultural_problems')
      .where('isActive', '==', true)
      .get();
    const results = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as AgriculturalProblem));
    allProblemsCache = { data: results, timestamp: Date.now() };
    return results;
  } catch (error) {
    console.error('Error fetching all problems:', error);
    return [];
  }
};

export const getActiveProductsByIds = async (productIds: string[]): Promise<Product[]> => {
  if (!db || !productIds || productIds.length === 0) return [];
  
  const missingIds = productIds.filter(id => !productsCache[id] || Date.now() - productsCache[id].timestamp >= CACHE_TTL);
  
  if (missingIds.length > 0) {
    try {
      // Chunking for Firestore 'in' query limit of 30
      for (let i = 0; i < missingIds.length; i += 30) {
        const chunk = missingIds.slice(i, i + 30);
        const snapshot = await db.collection('products')
          .where('isActive', '==', true)
          .where('__name__', 'in', chunk)
          .get();
        
        snapshot.docs.forEach(doc => {
          productsCache[doc.id] = { data: { id: doc.id, ...doc.data() } as Product, timestamp: Date.now() };
        });
      }
    } catch (error) {
      console.error('Error fetching products by ids:', error);
    }
  }
  
  return productIds.map(id => productsCache[id]?.data).filter((p): p is Product => Boolean(p));
};

/**
 * Enhanced Arabic text normalizer tailored for Yemeni agriculture:
 * - Removes diacritics & tatweel
 * - Normalizes Alef, Taa Marbuta, Alef Maksura, Hamzas
 * - Maps Yemeni dialects, regional synonyms, and colloquial agricultural terms
 */
export const normalizeArabicText = (text: string): string => {
  if (!text) return '';
  
  let normalized = text
    .replace(/[\u064B-\u065F\u0670]/g, '') // Remove diacritics / tashkeel
    .replace(/ـ+/g, '')                  // Remove tatweel / kashida
    .replace(/[إأآٱا]/g, 'ا')            // Normalize Alef variants
    .replace(/ة/g, 'ه')                  // Normalize Teh Marbuta
    .replace(/ى/g, 'ي')                  // Normalize Alef Maksura
    .replace(/ؤ/g, 'و')                  // Normalize Waw with Hamza
    .replace(/ئ/g, 'ي')                  // Normalize Yaa with Hamza
    .replace(/ء/g, '')                   // Strip isolated hamza
    .replace(/[؟?.,!،;:()\-]/g, ' ')     // Replace punctuation with space
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();

  // 1. Crop synonyms & dialect variations
  normalized = normalized
    .replace(/(^|\s)(بندوره|بندورة|طماطه|طماطة|قوطه|قوطة|البندوره|البندورة|الطماطه|القوطه)(\s|$)/g, '$1طماطم$3')
    .replace(/(^|\s)(شجره القات|شجرة القات|شجر القات|اغصان القات|عود القات|القات)(\s|$)/g, '$1قات$3')
    .replace(/(^|\s)(بطاط|البطاط|البطاطس)(\s|$)/g, '$1بطاطس$3')
    .replace(/(^|\s)(بصله|البصله|البصل)(\s|$)/g, '$1بصل$3')
    .replace(/(^|\s)(الخيار|خياره|خيارة)(\s|$)/g, '$1خيار$3');

  // 2. Pest & insect variations
  normalized = normalized
    .replace(/(^|\s)(حشره بيضاء|حشرة بيضاء|حشرات بيضاء|حشره بيضا|حشرات بيضا|دبان ابيض|دبانه بيضا|ذبابه بيضاء|ذبابة بيضاء|الذبابه البيضاء|الذبابة البيضاء)(\s|$)/g, '$1ذبابة بيضاء$3')
    .replace(/(^|\s)(عنكبوت احمر|عناكب حمراء|عنكبوتة حمرا|سوس احمر|حلم احمر|حلم|العنكبوت الاحمر)(\s|$)/g, '$1عنكبوت احمر$3')
    .replace(/(^|\s)(حشرات صغيره|حشرات صغيرة|حشرات صغار|دود صغير|ديدان صغيره|ديدان صغيرة|افات صغيره|افات صغيرة)(\s|$)/g, '$1افات حشرات$3')
    .replace(/(^|\s)(دوده|دودة|ديدان|دوده الحشد|دودة الحشد|دوده ورق|دودة ورق|دوده ثمار|دودة ثمار|الدوده)(\s|$)/g, '$1دودة$3')
    .replace(/(^|\s)(المن|من اسود|من اخضر|حشره المن|حشرة المن)(\s|$)/g, '$1من$3');

  // 3. Symptoms variations
  normalized = normalized
    .replace(/(^|\s)(ورق اصفر|ورق أصفر|اوراق صفراء|أوراق صفراء|ورقة صفراء|ورقه صفراء|ورقه صفرا|ورق يصفر|تصفر الاوراق|تصفر اوراقها|اوراقها تصفر|اصفرار الاوراق|اصفرار الأوراق|اصفرار الورق|يصفر|تصفر|اصفرت)(\s|$)/g, '$1اصفرار الاوراق$3')
    .replace(/(^|\s)(بقع بنيه|بقع بنية|البقع البنيه|البقع البنية|تبقع بني|نقط بنيه|نقط بنية|لطخات بنيه|لطخات بنية)(\s|$)/g, '$1بقع بنية$3')
    .replace(/(^|\s)(تعفن|عفن|متعفن|عفن اسود|عفن رمادي|عفن ابيض|عفن جذور|تعفن جذور|التعفن)(\s|$)/g, '$1تعفن$3')
    .replace(/(^|\s)(ذبول|ذابله|ذابلة|دابل|مذبل|يباس|جفاف الاوراق|جفاف الورق)(\s|$)/g, '$1ذبول$3')
    .replace(/(^|\s)(التفاف الاوراق|تلفف الاوراق|انكماش الاوراق|تجعد الاوراق|اوراق ملتفه|اوراق ملتفة)(\s|$)/g, '$1التفاف الاوراق$3');

  // 4. Intent & action variations (Yemeni & Arabic dialect question phrases)
  normalized = normalized
    .replace(/(^|\s)(ايش اسوي|ايش اسويله|ايش اسويلها|ايش اسوي له|ايش اسوي لها|كيف اسوي|كيف اتخلص|ايش الحل|ماهو الحل|وش الحل|ايش علاجها|ايش علاجه|ماهو العلاج|وش العلاج|شنو العلاج|كيف اعالج|علاجها ايش|علاجه ايش)(\s|$)/g, '$1علاج$3');

  return normalized.replace(/\s+/g, ' ').trim();
};

export interface MatchResult {
  problem: AgriculturalProblem;
  score: number;
  matchedCrop: Crop | null;
  matchReasons: string[];
}

export interface QueryAnalysisResult {
  intent: "AGRICULTURAL" | "GENERAL";
  matchedCrop: Crop | null;
  matches: MatchResult[];
  confidence: "HIGH" | "MEDIUM" | "NONE";
}

/**
 * Analyzes the user's message + recent conversation history:
 * 1. Checks current query and history for crops.
 * 2. Employs multi-factor scoring (crop, problem name, synonyms, symptoms, keywords, type).
 * 3. Categorizes confidence to avoid guessing and prevent hallucination.
 */
export const analyzeQuery = async (
  query: string,
  history?: { role: string, content: string }[]
): Promise<QueryAnalysisResult> => {
  const normalizedQuery = normalizeArabicText(query);
  const activeCrops = await getActiveCrops();

  // 1. Identify Crop (Check current query first, then history if not found)
  let matchedCrop: Crop | null = null;
  for (const crop of activeCrops) {
    const cropNames = [crop.name, ...(crop.synonyms || [])].map(normalizeArabicText);
    if (cropNames.some(name => normalizedQuery.includes(name))) {
      matchedCrop = crop;
      break;
    }
  }

  // If crop not mentioned in current query, look back in conversation history (context memory)
  if (!matchedCrop && history && history.length > 0) {
    const reversedHistory = [...history].reverse();
    for (const h of reversedHistory) {
      const normalizedHistoryText = normalizeArabicText(h.content || '');
      for (const crop of activeCrops) {
        const cropNames = [crop.name, ...(crop.synonyms || [])].map(normalizeArabicText);
        if (cropNames.some(name => normalizedHistoryText.includes(name))) {
          matchedCrop = crop;
          break;
        }
      }
      if (matchedCrop) break;
    }
  }

  // Keywords that indicate agricultural intent
  const agriKeywords = /زراع|محصول|نبات|سماد|مبيد|حشر|مرض|ورق|ثمر|قات|طماطم|شجر|جذر|ترب|سقي|ري|تعفن|اصفرار|ذبول|عنكبوت|دودة|دوده|بق|من|افة|آفة|علاج|رش|بقع/;
  const isAgricultural = matchedCrop !== null || agriKeywords.test(normalizedQuery);

  if (!isAgricultural) {
    return {
      intent: "GENERAL",
      matchedCrop: null,
      matches: [],
      confidence: "NONE"
    };
  }

  // 2. Fetch candidate problems
  let candidateProblems: AgriculturalProblem[] = [];
  if (matchedCrop) {
    candidateProblems = await getActiveProblemsForCrop(matchedCrop.id);
  } else {
    // If no crop was found, search across all problems to catch symptom-only queries
    candidateProblems = await getAllActiveProblems();
  }

  const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 2);
  const matchResults: MatchResult[] = [];

  for (const problem of candidateProblems) {
    let score = 0;
    const matchReasons: string[] = [];

    // Problem crop association
    const cropForThisProblem = matchedCrop || activeCrops.find(c => c.id === problem.cropId) || null;
    if (matchedCrop && problem.cropId === matchedCrop.id) {
      score += 15;
      matchReasons.push(`المحصول المطابق: ${matchedCrop.name}`);
    }

    // A. Problem Name matching
    const normProbName = normalizeArabicText(problem.name || '');
    if (normProbName && (normalizedQuery.includes(normProbName) || normProbName.split(/\s+/).every(w => normalizedQuery.includes(w)))) {
      score += 40;
      matchReasons.push(`تطابق اسم المشكلة: ${problem.name}`);
    } else if (normProbName && queryWords.some(qw => normProbName.includes(qw))) {
      score += 20;
      matchReasons.push(`تطابق جزئي لاسم المشكلة: ${problem.name}`);
    }

    // B. Synonyms matching
    const probSynonyms = (problem.synonyms || []).map(normalizeArabicText);
    for (const syn of probSynonyms) {
      if (!syn) continue;
      if (normalizedQuery.includes(syn)) {
        score += 30;
        matchReasons.push(`تطابق مرادف المشكلة: ${syn}`);
        break;
      }
    }

    // C. Type matching (e.g. حشرة, فطر, نقص عناصر)
    const normType = normalizeArabicText(problem.type || '');
    if (normType && normalizedQuery.includes(normType)) {
      score += 10;
      matchReasons.push(`تطابق نوع الإصابة: ${problem.type}`);
    }

    // D. Symptoms matching
    const probSymptoms = (problem.symptoms || []).map(normalizeArabicText);
    let matchedSymptomCount = 0;
    for (const sym of probSymptoms) {
      if (!sym) continue;
      if (normalizedQuery.includes(sym)) {
        score += 25;
        matchedSymptomCount++;
        matchReasons.push(`تطابق عرض دقيق: ${sym}`);
      } else {
        const symWords = sym.split(/\s+/).filter(w => w.length > 2);
        const hasWordMatch = symWords.some(sw => queryWords.some(qw => qw.includes(sw) || sw.includes(qw)));
        if (hasWordMatch) {
          score += 12;
          matchedSymptomCount++;
          matchReasons.push(`تطابق عرض مقارب: ${sym}`);
        }
      }
    }

    // E. Causes / Prevention keywords match
    const normCauses = normalizeArabicText(problem.causes || '');
    if (normCauses && queryWords.some(qw => normCauses.includes(qw))) {
      score += 5;
    }

    if (score > 0) {
      // Normalize score max 100
      const finalScore = Math.min(100, score);
      matchResults.push({
        problem,
        score: finalScore,
        matchedCrop: cropForThisProblem,
        matchReasons
      });
    }
  }

  // Sort descending by score
  matchResults.sort((a, b) => b.score - a.score);

  // Determine overall confidence
  let confidence: "HIGH" | "MEDIUM" | "NONE" = "NONE";
  if (matchResults.length > 0) {
    const topScore = matchResults[0].score;
    if (topScore >= 60) {
      confidence = "HIGH";
    } else if (topScore >= 35) {
      confidence = "MEDIUM";
    } else {
      confidence = "NONE";
    }
  }

  return {
    intent: "AGRICULTURAL",
    matchedCrop,
    matches: matchResults,
    confidence
  };
};

export const matchProblem = async (
  extractedCropName: string | null,
  extractedSymptoms: string[],
  extractedProblemType: string | null
): Promise<{ matches: MatchResult[], matchedCrop: Crop | null }> => {
  return analyzeQuery(extractedCropName || "");
};

