with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

bad = 'val startDestination = if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) "main" else "login"'
good = 'val startDestination = "main"'

content = content.replace(bad, good)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
