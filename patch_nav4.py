with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

profile_str = """            ProfileScreen(
                authRepository = authRepository,
                onBack = { navController.popBackStack() },
                onNavigateToFavorites = { navController.navigate("favorites") },
                onNavigateToOrders = { navController.navigate("myOrders") },
                onNavigateToAdmin = { navController.navigate("adminDashboard") },
                onLogout = {
                    authRepository.logout()
                    navController.navigate("login") {
                        popUpTo(0)
                    }
                }
            )"""
profile_str_new = """            ProfileScreen(
                authRepository = authRepository,
                onBack = { navController.popBackStack() },
                onNavigateToFavorites = { navController.navigate("favorites") },
                onNavigateToMyOrders = { navController.navigate("myOrders") }
            )"""

content = content.replace(profile_str, profile_str_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
