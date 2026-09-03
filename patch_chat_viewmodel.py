import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r", encoding="utf-8") as f:
    content = f.read()

msg_old = """    fun sendMessage(text: String) {
        if (text.isBlank()) return
        
        val userMsg = ChatMessageUi("""
msg_new = """    fun sendMessage(text: String) {
        if (text.isBlank() || _isLoading.value) return
        
        val userMsg = ChatMessageUi("""
content = content.replace(msg_old, msg_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w", encoding="utf-8") as f:
    f.write(content)
