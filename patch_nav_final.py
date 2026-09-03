with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("authRepository.isLoggedIn()", "authRepository.currentUser.value != null")

login_str = """            LoginScreen(
                onNavigateToRegister = { navController.navigate("register") },
                onNavigateToHome = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )"""
login_str_new = """            LoginScreen(
                authRepository = authRepository,
                onNavigateToRegister = { navController.navigate("register") },
                onLoginSuccess = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )"""

register_str = """            RegisterScreen(
                onNavigateToLogin = { navController.popBackStack() },
                onNavigateToHome = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )"""
register_str_new = """            RegisterScreen(
                authRepository = authRepository,
                onNavigateToLogin = { navController.popBackStack() },
                onRegisterSuccess = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )"""

guide_str = """            GuideScreen(
                onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                onNavigateToProblem = { id -> navController.navigate("problem/$id") },
                onNavigateToProduct = { id -> navController.navigate("product/$id") },
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToChat = { navController.navigate("conversations") }
            )"""
guide_str_new = """            GuideScreen(
                category = "crops",
                onBack = { navController.popBackStack() },
                onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                onNavigateToProblem = { id -> navController.navigate("problem/$id") }
            )"""

profile_str = """            ProfileScreen(
                onBack = { navController.popBackStack() },
                onNavigateToFavorites = { navController.navigate("favorites") },
                onNavigateToOrders = { navController.navigate("myOrders") },
                onNavigateToAdmin = { navController.navigate("adminDashboard") },
                onLogout = {
                    navController.navigate("login") {
                        popUpTo(0)
                    }
                }
            )"""
profile_str_new = """            ProfileScreen(
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

conversations_str = """            ConversationsScreen(
                onBack = { navController.popBackStack() },
                onNavigateToChat = { convId -> navController.navigate("chat?id=$convId") },
                onNewChat = { navController.navigate("chat") }
            )"""
conversations_str_new = """            ConversationsScreen(
                onBack = { navController.popBackStack() },
                onNavigateToChat = { convId -> navController.navigate("chat?id=$convId") }
            )"""

content = content.replace(login_str, login_str_new)
content = content.replace(register_str, register_str_new)
content = content.replace(guide_str, guide_str_new)
content = content.replace(profile_str, profile_str_new)
content = content.replace(conversations_str, conversations_str_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
