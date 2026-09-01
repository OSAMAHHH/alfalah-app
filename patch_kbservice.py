import re

with open("backend/src/services/knowledgeBaseService.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Enhance normalizeArabicText
old_normalize = """const normalizeArabicText = (text: string): string => {
  if (!text) return '';
  return text
    .replace(/[\u064B-\u065F]/g, '') // Remove diacritics
    .replace(/[إأآا]/g, 'ا')        // Normalize Alef
    .replace(/ة/g, 'ه')            // Normalize Teh Marbuta
    .replace(/ى/g, 'ي')            // Normalize Alef Maksura
    .trim()
    .toLowerCase();
};"""

new_normalize = """const normalizeArabicText = (text: string): string => {
  if (!text) return '';
  
  let normalized = text
    .replace(/[\u064B-\u065F]/g, '') // Remove diacritics
    .replace(/[إأآا]/g, 'ا')        // Normalize Alef
    .replace(/ة/g, 'ه')            // Normalize Teh Marbuta
    .replace(/ى/g, 'ي')            // Normalize Alef Maksura
    .trim()
    .toLowerCase();
    
  // Handle synonyms and common dialect variations requested
  normalized = normalized.replace(/بندوره/g, 'طماطم');
  normalized = normalized.replace(/حشره بيضاء/g, 'ذبابه بيضاء');
  normalized = normalized.replace(/الاوراق صفراء/g, 'اصفرار الورق');
  normalized = normalized.replace(/البقع البنيه/g, 'بقع بنيه');
  normalized = normalized.replace(/ال/g, ''); // Remove common "Al" for better matching of words like الاوراق -> اوراق

  return normalized;
};"""

content = content.replace(old_normalize, new_normalize)

# Update agriKeywords to include 'بندوره' 
content = content.replace("قات|طماطم|شجر", "قات|طماطم|بندوره|شجر")

with open("backend/src/services/knowledgeBaseService.ts", "w", encoding="utf-8") as f:
    f.write(content)
