import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

chat_composable_old = """            composable(Routes.CHAT) {
                if (FirebaseAuth.getInstance().currentUser == null) {
                    androidx.compose.runtime.LaunchedEffect(Unit) {
                        navController.navigate(Routes.LOGIN)
                    }
                } else {
                    ChatScreen(
                        conversationId = null,
                        onBack = { navController.popBackStack() }, 
                        onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                    ) 
                }
            }"""
            
chat_composable_new = """            composable(
                route = Routes.CHAT + "?initialQuery={initialQuery}",
                arguments = listOf(androidx.navigation.navArgument("initialQuery") { 
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
                    val initialQuery = backStackEntry.arguments?.getString("initialQuery")
                    ChatScreen(
                        conversationId = null,
                        initialQuery = initialQuery,
                        onBack = { navController.popBackStack() }, 
                        onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                    ) 
                }
            }"""
content = content.replace(chat_composable_old, chat_composable_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
