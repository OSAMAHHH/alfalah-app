import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add CHAT_ROUTE to Routes
routes_old = """object Routes {
    const val WELCOME = "welcome"
    const val LOGIN = "login"
    const val REGISTER = "register"
    const val HOME = "home"
    const val STORE = "store"
    const val CHAT = "chat" """
routes_new = """object Routes {
    const val WELCOME = "welcome"
    const val LOGIN = "login"
    const val REGISTER = "register"
    const val HOME = "home"
    const val STORE = "store"
    const val CHAT = "chat"
    const val CHAT_ROUTE = "chat?conversationId={conversationId}"
    fun chatWithId(id: String) = "chat?conversationId=$id" """
content = content.replace(routes_old, routes_new)

# Replace CHAT with CHAT_ROUTE in composable definition only
chat_composable_old = """            composable(Routes.CHAT) {
                if (FirebaseAuth.getInstance().currentUser == null) {
                    androidx.compose.runtime.LaunchedEffect(Unit) {
                        navController.navigate(Routes.LOGIN)
                    }
                } else {
                    ChatScreen(
                        onBack = { navController.popBackStack() }, 
                        onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                    ) 
                }
            }"""
chat_composable_new = """            composable(
                route = Routes.CHAT_ROUTE,
                arguments = listOf(androidx.navigation.navArgument("conversationId") { 
                    type = androidx.navigation.NavType.StringType
                    nullable = true
                    defaultValue = null
                })
            ) { backStackEntry ->
                if (FirebaseAuth.getInstance().currentUser == null) {
                    androidx.compose.runtime.LaunchedEffect(Unit) {
                        navController.navigate(Routes.LOGIN)
                    }
                } else {
                    val conversationId = backStackEntry.arguments?.getString("conversationId")
                    ChatScreen(
                        conversationId = conversationId,
                        onBack = { navController.popBackStack() }, 
                        onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                    ) 
                }
            }"""
content = content.replace(chat_composable_old, chat_composable_new)

# Fix ConversationsScreen navigation in AppNavigation.kt
content = content.replace('onNavigateToChat = { id -> navController.navigate(Routes.CHAT + "?conversationId=$id") }',
                          'onNavigateToChat = { id -> navController.navigate(Routes.chatWithId(id)) }')

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
