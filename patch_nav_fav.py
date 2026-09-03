import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

fav_old = """composable(Routes.FAVORITES) {
                FavoritesScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                )
            }"""
fav_new = """composable(Routes.FAVORITES) {
                FavoritesScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) },
                    onNavigateToCrop = { id -> navController.navigate(Routes.cropDetails(id)) },
                    onNavigateToProblem = { id -> navController.navigate(Routes.problemDetails(id)) }
                )
            }"""
content = content.replace(fav_old, fav_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
