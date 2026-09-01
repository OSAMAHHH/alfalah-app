import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add ChatMessageItem import
if "import com.example.alfalah.data.model.ChatMessageItem" not in content:
    content = content.replace("import com.example.alfalah.data.model.ChatMessage", "import com.example.alfalah.data.model.ChatMessage\nimport com.example.alfalah.data.model.ChatMessageItem")

# Remove searchLocalKnowledgeBase logic
start_remove = "val localResponse = searchLocalKnowledgeBase(text)"
end_remove = "return@launch\n            }"
if start_remove in content:
    content = re.sub(r'val localResponse = searchLocalKnowledgeBase\(text\).*?return@launch\s*\}', '', content, flags=re.DOTALL)

# Remove the private function searchLocalKnowledgeBase
content = re.sub(r'private suspend fun searchLocalKnowledgeBase.*?return null\s*\}', '', content, flags=re.DOTALL)

# Add historyItems extraction
history_logic = """
            val historyItems = _messages.value.takeLast(5).map { msg ->
                ChatMessageItem(
                    role = if (msg.isUser) "user" else "assistant",
                    content = msg.text
                )
            }
            val (responseText, productIds) = aiRepository.askAssistant(text, historyItems)
"""
content = content.replace("val (responseText, productIds) = aiRepository.askAssistant(text)", history_logic.strip())

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w", encoding="utf-8") as f:
    f.write(content)
