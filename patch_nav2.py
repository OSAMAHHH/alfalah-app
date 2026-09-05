with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

bad = """            composable("profile") {
                ProfileScreen(
                    authRepository = authRepository,
                    onBack = { navController.popBackStack() },
                    onNavigateToFavorites = { navController.navigate("favorites") },
                    onNavigateToMyOrders = { navController.navigate("myOrders") },
                    onNavigateToAdmin = { navController.navigate("adminDashboard") },
                    onLogout = onLogout
                )
            }"""

good = """            composable("profile") {
                ProfileScreen(
                    authRepository = authRepository,
                    onBack = { navController.popBackStack() },
                    onNavigateToFavorites = { navController.navigate("favorites") },
                    onNavigateToMyOrders = { navController.navigate("myOrders") },
                    onNavigateToAdmin = { navController.navigate("adminDashboard") },
                    onNavigateToSettings = { navController.navigate("settings") },
                    onNavigateToMyCrops = { navController.navigate("myCrops") },
                    onNavigateToConversations = { navController.navigate("conversations") },
                    onLogout = onLogout
                )
            }
            composable("settings") {
                com.example.alfalah.ui.screens.profile.SettingsScreen(
                    onBack = { navController.popBackStack() }
                )
            }
            composable("myCrops") {
                com.example.alfalah.ui.screens.profile.MyCropsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") }
                )
            }"""

content = content.replace(bad, good)
with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
