import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add to Routes
content = content.replace('    const val ADMIN_DASHBOARD = "admin_dashboard"', '    const val PROFILE = "profile"\n    const val ADMIN_DASHBOARD = "admin_dashboard"')

# Add imports for Profile
imports = """import com.example.alfalah.ui.screens.profile.ProfileScreen
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.outlined.Person"""
content = content.replace("import com.example.alfalah.ui.screens.auth.WelcomeScreen", "import com.example.alfalah.ui.screens.auth.WelcomeScreen\n" + imports)

# Update BottomNavItem list
old_nav_items = """val bottomNavItems = listOf(
    BottomNavItem(Routes.HOME, "الرئيسية", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem(Routes.STORE, "المتجر", Icons.Filled.Store, Icons.Outlined.Store),
    BottomNavItem(Routes.CHAT, "المساعد", Icons.Filled.SmartToy, Icons.Outlined.SmartToy)
)"""
new_nav_items = """val bottomNavItems = listOf(
    BottomNavItem(Routes.HOME, "الرئيسية", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem(Routes.STORE, "المتجر", Icons.Filled.Store, Icons.Outlined.Store),
    BottomNavItem(Routes.CHAT, "المساعد", Icons.Filled.SmartToy, Icons.Outlined.SmartToy),
    BottomNavItem(Routes.PROFILE, "حسابي", Icons.Filled.Person, Icons.Outlined.Person)
)"""
content = content.replace(old_nav_items, new_nav_items)

# Update showBottomBar
old_show = "val showBottomBar = currentRoute in listOf(Routes.HOME, Routes.STORE, Routes.CHAT)"
new_show = "val showBottomBar = currentRoute in listOf(Routes.HOME, Routes.STORE, Routes.CHAT, Routes.PROFILE)"
content = content.replace(old_show, new_show)

# Add composable
composable_profile = """
            composable(Routes.PROFILE) {
                if (FirebaseAuth.getInstance().currentUser == null) {
                    androidx.compose.runtime.LaunchedEffect(Unit) {
                        navController.navigate(Routes.LOGIN)
                    }
                } else {
                    ProfileScreen(
                        authRepository = authRepository,
                        onBack = { navController.popBackStack() }
                    )
                }
            }
"""
content = content.replace("composable(Routes.CHAT) {", composable_profile.strip() + "\n            composable(Routes.CHAT) {")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
