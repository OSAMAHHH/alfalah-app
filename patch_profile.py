with open("app/src/main/java/com/example/alfalah/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add onNavigateToAdmin to arguments
args_old = """    onNavigateToSettings: () -> Unit = {},
    onNavigateToMyOrders: () -> Unit = {}
) {"""
args_new = """    onNavigateToSettings: () -> Unit = {},
    onNavigateToMyOrders: () -> Unit = {},
    onNavigateToAdmin: () -> Unit = {},
    onLogout: () -> Unit = {}
) {"""
content = content.replace(args_old, args_new)

# Add admin button
items_old = """                    ProfileMenuItem(icon = Icons.Filled.ShoppingCart, title = "طلباتي", onClick = onNavigateToMyOrders)
                    ProfileMenuItem(icon = Icons.Filled.Chat, title = "محادثاتي السابقة", onClick = onNavigateToConversations)
                    ProfileMenuItem(icon = Icons.Filled.Settings, title = "الإعدادات", onClick = onNavigateToSettings)"""
items_new = """                    ProfileMenuItem(icon = Icons.Filled.ShoppingCart, title = "طلباتي", onClick = onNavigateToMyOrders)
                    ProfileMenuItem(icon = Icons.Filled.Chat, title = "محادثاتي السابقة", onClick = onNavigateToConversations)
                    ProfileMenuItem(icon = Icons.Filled.Settings, title = "الإعدادات", onClick = onNavigateToSettings)
                    if (currentUser?.role == "admin") {
                        ProfileMenuItem(icon = androidx.compose.material.icons.Icons.Filled.Person, title = "لوحة تحكم المشرف", onClick = onNavigateToAdmin)
                    }
                    ProfileMenuItem(icon = androidx.compose.material.icons.Icons.Filled.Person, title = "تسجيل الخروج", onClick = onLogout)"""
content = content.replace(items_old, items_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
