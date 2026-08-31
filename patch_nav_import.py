import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add route
if "IMPORT_DB" not in content:
    content = content.replace('val ADMIN_DASHBOARD = "admin_dashboard"', 'val ADMIN_DASHBOARD = "admin_dashboard"\n    val IMPORT_DB = "import_db"')

# Pass onNavigateToImport
content = content.replace("AdminDashboardScreen(onBack = { navController.popBackStack() })", "AdminDashboardScreen(onBack = { navController.popBackStack() }, onNavigateToImport = { navController.navigate(Routes.IMPORT_DB) })")

# Add composable(Routes.IMPORT_DB)
import_route = """
            composable(Routes.IMPORT_DB) {
                com.example.alfalah.ui.screens.admin.ImportDatabaseScreen(onBack = { navController.popBackStack() })
            }
"""
if "Routes.IMPORT_DB" not in content:
    content = content.replace("composable(Routes.ADMIN_DASHBOARD)", import_route + "\n            composable(Routes.ADMIN_DASHBOARD)")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
