with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("onNavigateToCheckout = { navController.navigate(\"checkout\") }", "onNavigateToCart = { navController.navigate(\"checkout\") }")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
