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
            }
            
            composable(Routes.CHAT) {
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

# A simpler approach: use regex to replace the specific block
content = re.sub(r'            composable\(Routes\.CHAT\)\s*\{[^\}]+\}\s*\}\s*else\s*\{\s*ChatScreen\(\s*onBack = \{ navController\.popBackStack\(\) \},\s*onNavigateToProduct = \{ id -> navController\.navigate\(Routes\.productDetails\(id\)\) \}\s*\)\s*\}\s*\}', chat_composable_new, content, count=1)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
