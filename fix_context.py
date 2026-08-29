import re
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

text = text.replace("fun AdminDashboardScreen(", "fun AdminDashboardScreen(\n    ")
text = re.sub(r'fun AdminDashboardScreen\([\s\S]*?\{', lambda m: m.group(0) + '\n    val context = androidx.compose.ui.platform.LocalContext.current\n', text)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
