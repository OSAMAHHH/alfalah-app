import re

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add ChatMessageItem
new_class = """
@JsonClass(generateAdapter = true)
data class ChatMessageItem(val role: String, val content: String)
"""

if "class ChatMessageItem" not in content:
    content = content.replace("@JsonClass(generateAdapter = true)\ndata class AiChatRequest", new_class + "\n@JsonClass(generateAdapter = true)\ndata class AiChatRequest")

# Modify AiChatRequest
old_ai_req = """data class AiChatRequest(
    val message: String,
    val conversationId: String = ""
)"""
new_ai_req = """data class AiChatRequest(
    val message: String,
    val conversationId: String = "",
    val history: List<ChatMessageItem> = emptyList()
)"""

content = content.replace(old_ai_req, new_ai_req)

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w", encoding="utf-8") as f:
    f.write(content)
