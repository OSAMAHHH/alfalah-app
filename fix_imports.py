with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Remove the broken imports at the very beginning
content = content.replace("import androidx.navigation.navArgument\nimport androidx.navigation.NavType\n", "")

# Insert them right after the package declaration
package_decl = "package com.example.alfalah.ui.navigation\n"
content = content.replace(package_decl, package_decl + "\nimport androidx.navigation.navArgument\nimport androidx.navigation.NavType\n")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
