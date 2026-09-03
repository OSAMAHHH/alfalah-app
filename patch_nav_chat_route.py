with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

chat_old = """        composable("chat?id={id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")
            ChatScreen(
                conversationId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") }
            )
        }
        composable("chat") {
            ChatScreen(
                conversationId = null,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") }
            )
        }"""
chat_new = """        composable(
            route = "chat?id={id}&initialQuery={initialQuery}",
            arguments = listOf(
                androidx.navigation.navArgument("id") { nullable = true },
                androidx.navigation.navArgument("initialQuery") { nullable = true }
            )
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")
            val query = backStackEntry.arguments?.getString("initialQuery")
            ChatScreen(
                conversationId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") },
                initialQuery = query
            )
        }"""

content = content.replace(chat_old, chat_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
