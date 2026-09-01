import re

with open("backend/src/types/index.ts", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "export interface AiChatRequest {\n  message: string;\n  conversationId?: string;\n}",
    "export interface AiChatRequest {\n  message: string;\n  conversationId?: string;\n  history?: { role: string, content: string }[];\n}"
)

content = content.replace(
    "export interface AiChatResponse {\n  answer: string;\n  recommendedProducts: string[];\n}",
    "export interface AiChatResponse {\n  answer: string;\n  recommendedProducts: string[];\n  source?: string;\n}"
)

with open("backend/src/types/index.ts", "w", encoding="utf-8") as f:
    f.write(content)
