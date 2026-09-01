import re

with open("backend/src/services/aiService.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the syntax error:
bad_code = """  return {
  let source: "KNOWLEDGE_BASE" | "GEMINI_WITH_KNOWLEDGE" | "GEMINI_GENERAL" = "GEMINI_GENERAL";"""

good_code = """  let source: "KNOWLEDGE_BASE" | "GEMINI_WITH_KNOWLEDGE" | "GEMINI_GENERAL" = "GEMINI_GENERAL";"""

content = content.replace(bad_code, good_code)

with open("backend/src/services/aiService.ts", "w", encoding="utf-8") as f:
    f.write(content)
