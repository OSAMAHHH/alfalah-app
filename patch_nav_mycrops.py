import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

mc_old = """composable(Routes.MY_CROPS) {
                MyCropsScreen(
                    onBack = { navController.popBackStack() }
                )
            }"""
mc_new = """composable(Routes.MY_CROPS) {
                MyCropsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToCrop = { id -> navController.navigate(Routes.cropDetails(id)) }
                )
            }"""
content = content.replace(mc_old, mc_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
