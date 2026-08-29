with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

text = text.replace("firestoreRepository: FirestoreRepository = remember {\n    val context = androidx.compose.ui.platform.LocalContext.current\n FirestoreRepository() }\n) {\n", "firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n) {\n    val context = androidx.compose.ui.platform.LocalContext.current\n")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
