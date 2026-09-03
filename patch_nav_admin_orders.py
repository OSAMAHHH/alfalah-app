with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

orders_str = """            AdminOrdersScreen(
                onBack = { navController.popBackStack() }
            )"""
orders_str_new = """            AdminOrdersScreen()"""

content = content.replace(orders_str, orders_str_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
