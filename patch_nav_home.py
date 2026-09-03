import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

old_home = """            composable(Routes.HOME) {
                HomeScreen(
                    authRepository = authRepository,
                    onNavigateToStore = { 
                        navController.navigate(Routes.STORE) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        } 
                    },
                    onNavigateToChat = { 
                        navController.navigate(Routes.CHAT) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        } 
                    },
                    onNavigateToAdmin = { navController.navigate(Routes.ADMIN_DASHBOARD) },
                    onNavigateToGuide = { category -> navController.navigate(Routes.guide(category)) },
                    onLogout = { 
                        navController.navigate(Routes.LOGIN) { 
                            popUpTo(Routes.HOME) { inclusive = true }
                        } 
                    }
                )
            }"""

new_home = """            composable(Routes.HOME) {
                HomeScreen(
                    authRepository = authRepository,
                    onNavigateToStore = { 
                        navController.navigate(Routes.STORE) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        } 
                    },
                    onNavigateToChat = { 
                        navController.navigate(Routes.CHAT) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        } 
                    },
                    onNavigateToAdmin = { navController.navigate(Routes.ADMIN_DASHBOARD) },
                    onNavigateToGuide = { category -> navController.navigate(Routes.guide(category)) },
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) },
                    onNavigateToCrop = { id -> navController.navigate(Routes.cropDetails(id)) },
                    onLogout = { 
                        navController.navigate(Routes.LOGIN) { 
                            popUpTo(Routes.HOME) { inclusive = true }
                        } 
                    }
                )
            }"""

content = content.replace(old_home, new_home)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
