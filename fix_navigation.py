with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

if "import com.example.alfalah.ui.screens.store.CartScreen" not in content:
    content = content.replace(
        "import com.example.alfalah.ui.screens.store.CheckoutScreen",
        "import com.example.alfalah.ui.screens.store.CheckoutScreen\nimport com.example.alfalah.ui.screens.store.CartScreen"
    )

if 'composable("cart")' not in content:
    content = content.replace(
        'composable("checkout") {',
        '''composable("cart") {
            CartScreen(
                onBack = { navController.popBackStack() },
                onCheckout = { navController.navigate("checkout") }
            )
        }
        composable("checkout") {'''
    )

content = content.replace(
    'onNavigateToCart = { navController.navigate("checkout") }',
    'onNavigateToCart = { navController.navigate("cart") }'
)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
