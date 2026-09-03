import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

chat_sig_old = """@Composable
fun ChatScreen(
    conversationId: String?,
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ChatViewModel = viewModel()
) {"""

chat_sig_new = """@Composable
fun ChatScreen(
    conversationId: String?,
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ChatViewModel = viewModel(),
    initialQuery: String? = null
) {"""
content = content.replace(chat_sig_old, chat_sig_new)

chat_effect_old = """    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
    }"""
chat_effect_new = """    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
        if (!initialQuery.isNullOrEmpty()) {
            viewModel.sendMessage(initialQuery)
        }
    }"""
content = content.replace(chat_effect_old, chat_effect_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
