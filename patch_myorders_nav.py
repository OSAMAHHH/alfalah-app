import re

with open("app/src/main/java/com/example/alfalah/MainActivity.kt", "r") as f:
    content = f.read()

# Make sure imports are there
if "com.example.alfalah.ui.screens.profile.MyOrdersScreen" not in content:
    content = content.replace(
        "import com.example.alfalah.ui.screens.store.CheckoutScreen",
        "import com.example.alfalah.ui.screens.store.CheckoutScreen\nimport com.example.alfalah.ui.screens.profile.MyOrdersScreen"
    )

if 'composable("settings")' in content and 'composable("my_orders")' not in content:
    content = content.replace(
        'SettingsScreen(\n                                    onNavigateToLogin = {',
        'SettingsScreen(\n                                    onNavigateToMyOrders = { navController.navigate("my_orders") },\n                                    onNavigateToLogin = {'
    )

    my_orders_nav = """
                            composable("my_orders") {
                                MyOrdersScreen(
                                    onBack = { navController.popBackStack() }
                                )
                            }
"""
    content = content.replace('composable("admin") {', my_orders_nav + '                            composable("admin") {')

with open("app/src/main/java/com/example/alfalah/MainActivity.kt", "w") as f:
    f.write(content)
