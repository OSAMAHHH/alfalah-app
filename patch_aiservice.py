import re

with open("backend/src/services/aiService.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Add history extraction
content = content.replace("const apiKey = process.env.GEMINI_API_KEY;", "const apiKey = process.env.GEMINI_API_KEY;\n  const { message, history } = request;")
content = content.replace("const { intent, matchedCrop, matches } = await analyzeQuery(request.message);", "const { intent, matchedCrop, matches } = await analyzeQuery(message);")

# Update prompt to use history if available
prompt_building_old = """  const finalPrompt = `
    معلومات وتوجيهات لك (لا تذكرها للمستخدم مباشرة، بل نفذها):
    ${systemContext}
    
    سؤال المستخدم: "${request.message}"
  `;"""

prompt_building_new = """  // Format history if exists
  let historyText = "";
  if (history && history.length > 0) {
    historyText = "تاريخ المحادثة السابقة:\\n" + history.map(h => `${h.role === 'user' ? 'المستخدم' : 'المساعد'}: ${h.content}`).join("\\n") + "\\n\\n";
  }

  const finalPrompt = `
    معلومات وتوجيهات لك (لا تذكرها للمستخدم مباشرة، بل نفذها):
    ${systemContext}
    
    ${historyText}
    سؤال المستخدم: "${message}"
  `;
"""
content = content.replace(prompt_building_old, prompt_building_new)

# Add Source logic
source_logic_old = """    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds
  };"""

source_logic_new = """  let source: "KNOWLEDGE_BASE" | "GEMINI_WITH_KNOWLEDGE" | "GEMINI_GENERAL" = "GEMINI_GENERAL";
  if (intent === "AGRICULTURAL") {
    if (matchedCrop && matches.length > 0) {
      source = "GEMINI_WITH_KNOWLEDGE"; // or KNOWLEDGE_BASE conceptually
    } else {
      source = "GEMINI_GENERAL";
    }
  }

  return {
    answer: finalResponse.text || "عذراً، حدث خطأ أثناء صياغة الإجابة.",
    recommendedProducts: finalRecommendedProductIds,
    source
  };"""

content = content.replace(source_logic_old, source_logic_new)

with open("backend/src/services/aiService.ts", "w", encoding="utf-8") as f:
    f.write(content)
