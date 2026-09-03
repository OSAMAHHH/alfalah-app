import re

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

# Add onNavigateToMyCrops to HomeScreen parameters
content = content.replace(
    'onNavigateToCrop: (String) -> Unit = {},',
    'onNavigateToCrop: (String) -> Unit = {},\n    onNavigateToMyCrops: () -> Unit = {},'
)

# Fix the My Crops View All button
content = content.replace(
    'TextButton(onClick = { /* Navigate to MyCrops which is in Profile actually, or we can just navigate to MY_CROPS route */ })',
    'TextButton(onClick = onNavigateToMyCrops)'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    nav_content = f.read()

nav_content = nav_content.replace(
    'onNavigateToGuide = { category -> navController.navigate(Routes.guide(category)) },',
    'onNavigateToGuide = { category -> navController.navigate(Routes.guide(category)) },\n                    onNavigateToMyCrops = { navController.navigate(Routes.MY_CROPS) },'
)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(nav_content)

