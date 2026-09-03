import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Add constants to Routes
routes_add = """    const val PROFILE = "profile"
    const val CART = "cart"
    const val CHECKOUT = "checkout"
    const val MY_ORDERS = "my_orders\""""

content = content.replace('    const val PROFILE = "profile"', routes_add)

# Update STORE composable
store_old = """            composable(Routes.STORE) { 
                StoreScreen(
                    onBack = { navController.popBackStack() }, 
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                ) 
            }"""

store_new = """            composable(Routes.STORE) { 
                StoreScreen(
                    onBack = { navController.popBackStack() }, 
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) },
                    onNavigateToCart = { navController.navigate(Routes.CART) }
                ) 
            }"""

content = content.replace(store_old, store_new)


# Update PRODUCT_DETAILS composable
pd_old = """            composable(Routes.PRODUCT_DETAILS) { backStackEntry ->
                val productId = backStackEntry.arguments?.getString("productId") ?: ""
                ProductDetailsScreen(
                    productId = productId, 
                    onBack = { navController.popBackStack() }
                )
            }"""

pd_new = """            composable(Routes.PRODUCT_DETAILS) { backStackEntry ->
                val productId = backStackEntry.arguments?.getString("productId") ?: ""
                ProductDetailsScreen(
                    productId = productId, 
                    onBack = { navController.popBackStack() },
                    onNavigateToCart = { navController.navigate(Routes.CART) }
                )
            }"""

content = content.replace(pd_old, pd_new)

# Update SETTINGS composable
settings_old = """            composable(Routes.SETTINGS) {
                SettingsScreen(
                    onBack = { navController.popBackStack() },
                    onLogout = {
                        authRepository.logout()
                        navController.navigate(Routes.LOGIN) {
                            popUpTo(0)
                        }
                    }
                )
            }"""

settings_new = """            composable(Routes.SETTINGS) {
                SettingsScreen(
                    onBack = { navController.popBackStack() },
                    onLogout = {
                        authRepository.logout()
                        navController.navigate(Routes.LOGIN) {
                            popUpTo(0)
                        }
                    },
                    onNavigateToMyOrders = { navController.navigate(Routes.MY_ORDERS) }
                )
            }"""
content = content.replace(settings_old, settings_new)

# Add CART, CHECKOUT, MY_ORDERS composables
composables_to_add = """            composable(Routes.CART) {
                com.example.alfalah.ui.screens.store.CartScreen(
                    onBack = { navController.popBackStack() },
                    onCheckout = { navController.navigate(Routes.CHECKOUT) }
                )
            }
            composable(Routes.CHECKOUT) {
                com.example.alfalah.ui.screens.store.CheckoutScreen(
                    onBack = { navController.popBackStack() },
                    onOrderSuccess = { 
                        navController.navigate(Routes.MY_ORDERS) {
                            popUpTo(Routes.STORE) { inclusive = false }
                        }
                    }
                )
            }
            composable(Routes.MY_ORDERS) {
                com.example.alfalah.ui.screens.profile.MyOrdersScreen(
                    onBack = { navController.popBackStack() }
                )
            }
        }
    }
}"""

content = content.replace("        }\n    }\n}", composables_to_add)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
