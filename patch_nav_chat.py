with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

crop_str = """            CropDetailsScreen(
                cropId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProblem = { pId -> navController.navigate("problem/$pId") }
            )"""
crop_str_new = """            CropDetailsScreen(
                cropId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProblem = { pId -> navController.navigate("problem/$pId") },
                onNavigateToChatWithQuery = { query -> navController.navigate("chat?initialQuery=$query") }
            )"""

problem_str = """            ProblemDetailsScreen(
                problemId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") }
            )"""
problem_str_new = """            ProblemDetailsScreen(
                problemId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") },
                onNavigateToChatWithQuery = { query -> navController.navigate("chat?initialQuery=$query") }
            )"""

content = content.replace(crop_str, crop_str_new)
content = content.replace(problem_str, problem_str_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
