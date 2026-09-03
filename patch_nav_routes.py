import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('const val CHAT = "chat"', 'const val CHAT = "chat"\n    const val CHAT_ROUTE = "chat?conversationId={conversationId}"\n    fun chatWithId(id: String) = "chat?conversationId=$id"')

# Update Chat composable error
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

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
