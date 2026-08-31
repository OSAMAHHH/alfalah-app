import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

content = re.sub(r'fun AdminDashboardScreen\(\s*onBack:\s*\(\)\s*->\s*Unit,\s*modifier:\s*Modifier\s*=\s*Modifier,\s*firestoreRepository:\s*FirestoreRepository\s*=\s*remember\s*\{\s*FirestoreRepository\(\)\s*\}\s*\)\s*\{', 
"""fun AdminDashboardScreen(
    onBack: () -> Unit,
    onNavigateToImport: () -> Unit = {},
    modifier: Modifier = Modifier,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {""", content)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
