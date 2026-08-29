with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

import re
text = re.sub(r'firestoreRepository: FirestoreRepository = remember \{\s*val context = androidx\.compose\.ui\.platform\.LocalContext\.current\s*FirestoreRepository\(\) \}\s*\)', 'firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n)', text)
text = text.replace("firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n) {", "firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n) {\n    val context = androidx.compose.ui.platform.LocalContext.current\n")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
