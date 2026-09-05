with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

bad = """                HomeScreen(
                    onNavigateToGuide = { cat -> navController.navigate("guide") },
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                    onNavigateToProduct = { id -> navController.navigate("product/$id") },
                    onNavigateToStore = { navController.navigate("store") }, // Need a store screen? Just guide for now
                    onNavigateToAdmin = { navController.navigate("adminDashboard") }
                )"""

good = """                HomeScreen(
                    authRepository = authRepository,
                    onNavigateToGuide = { cat -> navController.navigate("guide") },
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                    onNavigateToProduct = { id -> navController.navigate("product/$id") },
                    onNavigateToStore = { navController.navigate("guide") },
                    onNavigateToAdmin = { navController.navigate("adminDashboard") },
                    onNavigateToChat = { navController.navigate("conversations") },
                    onNavigateToCart = { navController.navigate("cart") },
                    onLogout = onLogout
                )"""

content = content.replace(bad, good)
with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
