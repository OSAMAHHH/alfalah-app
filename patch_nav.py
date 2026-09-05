with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

bad_nav_1 = """                    onNavigateToStore = { navController.navigate("guide") },"""
good_nav_1 = """                    onNavigateToStore = { navController.navigate("store") },"""

content = content.replace(bad_nav_1, good_nav_1)

bad_nav_2 = """            composable("guide") {"""
good_nav_2 = """            composable("store") {
                com.example.alfalah.ui.screens.store.StoreScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToProduct = { id -> navController.navigate("product/$id") },
                    onNavigateToCart = { navController.navigate("cart") }
                )
            }
            composable("guide") {"""

content = content.replace(bad_nav_2, good_nav_2)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
