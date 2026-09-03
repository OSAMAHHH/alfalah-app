with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("currentConversation?.messages ?: emptyList()", "currentConversation?.messages ?: emptyList<com.example.alfalah.data.model.ChatMessage>()")

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
