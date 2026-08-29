import { db } from '../config/firebase';
import { Crop, AgriculturalProblem, Product } from '../types';

// --- In-Memory Caches ---
let cropsCache: { data: Crop[], timestamp: number } | null = null;
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
    console.error('Error fetching problems:', error);
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
  
  return productIds.map(id => productsCache[id]?.data).filter(Boolean);
};

// Normalizes Arabic text for better matching
const normalizeArabicText = (text: string): string => {
  if (!text) return '';
  return text
    .replace(/[\u064B-\u065F]/g, '') // Remove diacritics
    .replace(/[إأآا]/g, 'ا')        // Normalize Alef
    .replace(/ة/g, 'ه')            // Normalize Teh Marbuta
    .replace(/ى/g, 'ي')            // Normalize Alef Maksura
    .trim()
    .toLowerCase();
};

export interface MatchResult {
  problem: AgriculturalProblem;
  score: number;
}

export const analyzeQuery = async (query: string): Promise<{ intent: string, matchedCrop: Crop | null, matches: MatchResult[] }> => {
  const normalizedQuery = normalizeArabicText(query);
  const activeCrops = await getActiveCrops();
  
  let matchedCrop: Crop | null = null;
  for (const crop of activeCrops) {
    const cropNames = [crop.name, ...(crop.synonyms || [])].map(normalizeArabicText);
    if (cropNames.some(name => normalizedQuery.includes(name))) {
      matchedCrop = crop;
      break;
    }
  }

  // Keywords that indicate agricultural intent
  const agriKeywords = /زراع|محصول|نبات|سماد|مبيد|حشر|مرض|ورق|ثمر|قات|طماطم|شجر|جذر|ترب|سقي|ري|تعفن|اصفرار|ذبول|عنكبوت|دودة|بق|من/;
  const isAgricultural = matchedCrop !== null || agriKeywords.test(normalizedQuery);

  if (!isAgricultural) {
    return { intent: "GENERAL", matchedCrop: null, matches: [] };
  }

  const matchResults: MatchResult[] = [];
  if (matchedCrop) {
    const problems = await getActiveProblemsForCrop(matchedCrop.id);
    const queryWords = normalizedQuery.split(/\s+/).filter(w => w.length > 2);
    
    for (const problem of problems) {
      let score = 40; // Base score
      
      const pType = normalizeArabicText(problem.type || '');
      if (pType && normalizedQuery.includes(pType)) score += 10;
      
      const problemSymptoms = [...(problem.symptoms || []), ...(problem.synonyms || [])].map(normalizeArabicText);
      let symptomMatchCount = 0;
      
      for (const sym of problemSymptoms) {
        if (!sym) continue;
        if (normalizedQuery.includes(sym)) {
          symptomMatchCount += 2;
          continue;
        }
        const symWords = sym.split(/\s+/).filter(w => w.length > 2);
        if (symWords.some(sw => queryWords.some(qw => qw.includes(sw) || sw.includes(qw)))) {
          symptomMatchCount += 1;
        }
      }
      
      if (problemSymptoms.length > 0) {
        const matchRatio = symptomMatchCount / Math.max(1, problemSymptoms.length);
        score += Math.min(50, matchRatio * 50);
      }
      
      matchResults.push({ problem, score });
    }
    matchResults.sort((a, b) => b.score - a.score);
  }

  return { intent: "AGRICULTURAL", matchedCrop, matches: matchResults };
};

// Kept for backward compatibility if used elsewhere
export const matchProblem = async (
  extractedCropName: string | null,
  extractedSymptoms: string[],
  extractedProblemType: string | null
): Promise<{ matches: MatchResult[], matchedCrop: Crop | null }> => {
  return analyzeQuery(extractedCropName || "");
};
