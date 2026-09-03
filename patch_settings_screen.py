import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "r") as f:
    content = f.read()

# Make onNavigateToMyOrders functional
content = content.replace(
    'fun SettingsScreen(\n    onNavigateToLogin: () -> Unit,\n    modifier: Modifier = Modifier,\n    authRepository: AuthRepository = remember { AuthRepository() }\n)',
    'fun SettingsScreen(\n    onNavigateToLogin: () -> Unit,\n    onNavigateToMyOrders: () -> Unit = {},\n    modifier: Modifier = Modifier,\n    authRepository: AuthRepository = remember { AuthRepository() }\n)'
)

button = """
                item {
                    SettingsItem(
                        icon = androidx.compose.material.icons.Icons.Outlined.ShoppingCart,
                        title = "طلباتي",
                        onClick = onNavigateToMyOrders
                    )
                }
"""

content = content.replace(
    'item {\n                    SettingsItem(\n                        icon = Icons.Outlined.LocationOn,',
    button.strip() + '\n                }\n                item {\n                    SettingsItem(\n                        icon = Icons.Outlined.LocationOn,'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "w") as f:
    f.write(content)
