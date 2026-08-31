import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import_route = """
            composable(Routes.IMPORT_DB) {
                com.example.alfalah.ui.screens.admin.ImportDatabaseScreen(onBack = { navController.popBackStack() })
            }
"""

content = content.replace("composable(Routes.ADMIN_DASHBOARD)", import_route.strip() + "\n            composable(Routes.ADMIN_DASHBOARD)")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
