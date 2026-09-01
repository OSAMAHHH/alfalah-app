export interface AiChatRequest {
  message: string;
  conversationId?: string;
  history?: { role: string, content: string }[];
}

export interface AiChatResponse {
  answer: string;
  recommendedProducts: string[];
  source?: string;
}

export interface BaseEntity {
  isActive?: boolean;
  createdAt?: string;
  updatedAt?: string;
  createdBy?: string;
  updatedBy?: string;
}

export interface Product extends BaseEntity {
  id: string;
  name: string;
  imageUrl: string;
  description: string;
  price: number;
  category: string;
  nutrients: string[];
  suitableCrops: string[];
  suitableProblems: string[];
  usage: string;
  dosage: string;
  warnings: string;
  stock: number;
  tested: boolean;
  recommended: boolean;
}

export interface Crop extends BaseEntity {
  id: string;
  name: string;
  synonyms: string[];
  description: string;
}

export interface AgriculturalProblem extends BaseEntity {
  id: string;
  cropId: string;
  name: string;
  synonyms: string[];
  type: string; // e.g., 'disease', 'pest', 'deficiency'
  symptoms: string[];
  causes: string;
  prevention: string;
  treatment: string;
  recommendedProductIds: string[];
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}
