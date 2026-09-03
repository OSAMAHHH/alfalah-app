import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports for new screens
imports_old = "import com.example.alfalah.ui.screens.guide.GuideScreen"
imports_new = """import com.example.alfalah.ui.screens.guide.GuideScreen
import com.example.alfalah.ui.screens.guide.CropDetailsScreen
import com.example.alfalah.ui.screens.guide.ProblemDetailsScreen"""
content = content.replace(imports_old, imports_new)

# Update GuideScreen call
guide_old = """            composable(Routes.GUIDE) { backStackEntry ->
                val category = backStackEntry.arguments?.getString("category") ?: ""
                GuideScreen(category = category, onBack = { navController.popBackStack() })
            }"""
guide_new = """            composable(Routes.GUIDE) { backStackEntry ->
                val category = backStackEntry.arguments?.getString("category") ?: ""
                GuideScreen(
                    category = category, 
                    onBack = { navController.popBackStack() },
                    onNavigateToCrop = { id -> navController.navigate(Routes.cropDetails(id)) },
                    onNavigateToProblem = { id -> navController.navigate(Routes.problemDetails(id)) }
                )
            }
            
            composable(Routes.CROP_DETAILS) { backStackEntry ->
                val cropId = backStackEntry.arguments?.getString("cropId") ?: ""
                CropDetailsScreen(
                    cropId = cropId,
                    onBack = { navController.popBackStack() },
                    onNavigateToProblem = { id -> navController.navigate(Routes.problemDetails(id)) },
                    onNavigateToChatWithQuery = { query -> 
                        navController.navigate(Routes.CHAT + "?initialQuery=$query") 
                    }
                )
            }
            
            composable(Routes.PROBLEM_DETAILS) { backStackEntry ->
                val problemId = backStackEntry.arguments?.getString("problemId") ?: ""
                ProblemDetailsScreen(
                    problemId = problemId,
                    onBack = { navController.popBackStack() },
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) },
                    onNavigateToChatWithQuery = { query -> 
                        navController.navigate(Routes.CHAT + "?initialQuery=$query") 
                    }
                )
            }"""
content = content.replace(guide_old, guide_new)

# Add initialQuery arg to CHAT route
chat_route_old = 'const val CHAT = "chat"'
chat_route_new = 'const val CHAT = "chat"\n    const val CHAT_INITIAL = "chat?initialQuery={initialQuery}"'
# Actually I already modified Routes, let's just make it simple: 
# The CHAT route is "chat", we can add another route or just define it in CHAT composable.

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
