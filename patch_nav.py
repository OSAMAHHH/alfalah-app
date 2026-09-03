with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import_str = "import com.example.alfalah.ui.screens.admin.AdminOrdersScreen"
import_str_new = "import com.example.alfalah.ui.screens.admin.AdminOrdersScreen\nimport com.example.alfalah.ui.screens.admin.ImportDatabaseScreen"

add_nav = """        composable("importDb") {
            ImportDatabaseScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}"""

content = content.replace(import_str, import_str_new)
content = content.replace("    }\n}", add_nav)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
