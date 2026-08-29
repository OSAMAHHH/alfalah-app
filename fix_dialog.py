with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

text = text.replace("@Composable\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ProductDialog", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ProductDialog")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
