import { db } from '../config/firebase';
import { Crop, AgriculturalProblem, Product } from '../types';

export const getActiveCrops = async (): Promise<Crop[]> => {
  if (!db) return [];
  try {
    const snapshot = await db.collection('crops').where('isActive', '==', true).get();
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Crop));
  } catch (error) {
    console.error('Error fetching crops:', error);
    return [];
  }
};

export const getActiveProblemsForCrop = async (cropId: string): Promise<AgriculturalProblem[]> => {
  if (!db) return [];
  try {
    const snapshot = await db.collection('agricultural_problems')
      .where('cropId', '==', cropId)
      .where('isActive', '==', true)
      .get();
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as AgriculturalProblem));
  } catch (error) {
    console.error('Error fetching problems:', error);
    return [];
  }
};

export const getActiveProductsByIds = async (productIds: string[]): Promise<Product[]> => {
  if (!db || !productIds || productIds.length === 0) return [];
  try {
    // Firestore 'in' query supports up to 30 elements. We assume productIds <= 30.
    const snapshot = await db.collection('products')
      .where('isActive', '==', true)
      .where('__name__', 'in', productIds.slice(0, 30))
      .get();
    
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Product));
  } catch (error) {
    console.error('Error fetching products by ids:', error);
    return [];
  }
};

// Normalizes Arabic text for better matching (removes diacritics, normalizes alef, teh marbuta)
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

export const matchProblem = async (
  extractedCropName: string | null,
  extractedSymptoms: string[],
  extractedProblemType: string | null
): Promise<{ matches: MatchResult[], matchedCrop: Crop | null }> => {
  
  if (!extractedCropName) return { matches: [], matchedCrop: null };

  const activeCrops = await getActiveCrops();
  const normalizedExtractedCrop = normalizeArabicText(extractedCropName);

  // 1. Find crop match
  let matchedCrop: Crop | null = null;
  for (const crop of activeCrops) {
    const cropNames = [crop.name, ...(crop.synonyms || [])].map(normalizeArabicText);
    if (cropNames.some(name => name.includes(normalizedExtractedCrop) || normalizedExtractedCrop.includes(name))) {
      matchedCrop = crop;
      break;
    }
  }

  if (!matchedCrop) {
    return { matches: [], matchedCrop: null };
  }

  // 2. Fetch problems for matched crop
  const problems = await getActiveProblemsForCrop(matchedCrop.id);
  const matchResults: MatchResult[] = [];

  const normalizedExtractedSymptoms = extractedSymptoms.map(normalizeArabicText);
  const normalizedExtractedType = extractedProblemType ? normalizeArabicText(extractedProblemType) : '';

  for (const problem of problems) {
    let score = 40; // Base score for crop match

    // Problem Type Match (10 points)
    if (normalizedExtractedType) {
      const pType = normalizeArabicText(problem.type || '');
      if (pType && (pType.includes(normalizedExtractedType) || normalizedExtractedType.includes(pType))) {
        score += 10;
      }
    }

    // Symptoms Match (50 points)
    const problemSymptoms = [...(problem.symptoms || []), ...(problem.synonyms || [])].map(normalizeArabicText);
    let symptomMatchCount = 0;
    
    for (const extSymptom of normalizedExtractedSymptoms) {
      // Partial match for symptoms
      if (problemSymptoms.some(ps => ps.includes(extSymptom) || extSymptom.includes(ps))) {
        symptomMatchCount++;
      }
    }

    if (normalizedExtractedSymptoms.length > 0) {
      const symptomScore = (symptomMatchCount / normalizedExtractedSymptoms.length) * 50;
      score += symptomScore;
    }

    matchResults.push({ problem, score });
  }

  // Sort by score descending
  matchResults.sort((a, b) => b.score - a.score);

  return { matches: matchResults, matchedCrop };
};
