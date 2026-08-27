import { db } from '../config/firebase';
import { Product } from '../types';

/**
 * Service to interact with the products collection in Firestore.
 * This sets the foundation for the future Recommendation Engine.
 */
export const getAllProducts = async (): Promise<Product[]> => {
  if (!db) {
    throw new Error('Firestore is not initialized.');
  }

  try {
    const snapshot = await db.collection('products').get();
    const products: Product[] = [];
    
    snapshot.forEach((doc) => {
      const data = doc.data();
      products.push({
        id: doc.id,
        name: data.name || '',
        imageUrl: data.imageUrl || '',
        description: data.description || '',
        price: data.price || 0,
        category: data.category || '',
        nutrients: data.nutrients || [],
        suitableCrops: data.suitableCrops || [],
        suitableProblems: data.suitableProblems || [],
        usage: data.usage || '',
        dosage: data.dosage || '',
        warnings: data.warnings || '',
        stock: data.stock || 0,
        tested: data.tested || false,
        recommended: data.recommended || false
      });
    });

    return products;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw new Error('Failed to fetch products');
  }
};
