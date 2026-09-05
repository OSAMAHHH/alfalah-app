with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val startDestination = if (authRepository.currentUser.value != null) "guide" else "login"',
    'val startDestination = if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) "guide" else "login"'
)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
