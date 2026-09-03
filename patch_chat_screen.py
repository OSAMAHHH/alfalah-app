import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

screen_sig_old = """@Composable
fun ChatScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ChatViewModel = viewModel()
) {"""

screen_sig_new = """@Composable
fun ChatScreen(
    conversationId: String?,
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ChatViewModel = viewModel()
) {
    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
    }
"""
content = content.replace(screen_sig_old, screen_sig_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
