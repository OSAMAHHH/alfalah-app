with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("onNavigateToOrders = { navController.navigate(\"adminOrders\") }", "")
content = content.replace("onNavigateToImport = { navController.navigate(\"importDb\") },\n                \n            )", "onNavigateToImport = { navController.navigate(\"importDb\") }\n            )")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
