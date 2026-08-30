import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    text = f.read()

# Add WELCOME to Routes
text = text.replace('const val LOGIN = "login"', 'const val WELCOME = "welcome"\n    const val LOGIN = "login"')

# Import WelcomeScreen
text = text.replace('import com.example.alfalah.ui.screens.auth.RegisterScreen', 'import com.example.alfalah.ui.screens.auth.RegisterScreen\nimport com.example.alfalah.ui.screens.auth.WelcomeScreen')

# Change startDestination logic
old_start = '''    val startDestination = remember {
        if (FirebaseAuth.getInstance().currentUser != null) Routes.HOME else Routes.LOGIN
    }'''
new_start = '''    val startDestination = remember {
        if (FirebaseAuth.getInstance().currentUser != null) Routes.HOME else Routes.WELCOME
    }'''
text = text.replace(old_start, new_start)

# Add WELCOME composable before LOGIN
welcome_composable = '''
            composable(Routes.WELCOME) {
                WelcomeScreen(
                    onNavigateToLogin = { navController.navigate(Routes.LOGIN) },
                    onNavigateToHomeAsGuest = { 
                        navController.navigate(Routes.HOME) {
                            popUpTo(Routes.WELCOME) { inclusive = true }
                        }
                    }
                )
            }'''
text = text.replace('composable(Routes.LOGIN) {', welcome_composable + '\n            composable(Routes.LOGIN) {')

# Modify Chat and other protected routes
chat_composable_old = '''            composable(Routes.CHAT) { 
                ChatScreen(
                    onBack = { navController.popBackStack() }, 
                    onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                ) 
            }'''
chat_composable_new = '''            composable(Routes.CHAT) { 
                if (FirebaseAuth.getInstance().currentUser == null) {
                    androidx.compose.runtime.LaunchedEffect(Unit) {
                        navController.navigate(Routes.LOGIN)
                    }
                } else {
                    ChatScreen(
                        onBack = { navController.popBackStack() }, 
                        onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
                    ) 
                }
            }'''
text = text.replace(chat_composable_old, chat_composable_new)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(text)
