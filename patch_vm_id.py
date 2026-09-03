import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r", encoding="utf-8") as f:
    content = f.read()

save_logic_old = """            val saveResult = userServicesRepository.saveConversation(conv)
            if (currentConversationId.isNullOrEmpty()) {
                // We'd ideally reload to get the new ID, but skipping for simplicity
                // In a proper implementation, saveConversation would return the ID
            }"""

save_logic_new = """            val saveResult = userServicesRepository.saveConversation(conv)
            if (currentConversationId.isNullOrEmpty() && saveResult.isSuccess) {
                currentConversationId = saveResult.getOrNull()
            }"""
content = content.replace(save_logic_old, save_logic_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w", encoding="utf-8") as f:
    f.write(content)
