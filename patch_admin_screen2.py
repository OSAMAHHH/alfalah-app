import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

broken_section = """    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                title = { Text("لوحة تحكم المشرف") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "رجوع")
                    }
                },
                actions = {
                    IconButton(onClick = onNavigateToImport) {
                        Icon(androidx.compose.material.icons.Icons.Filled.UploadFile, contentDescription = "استيراد")
                    }
                }
            )
                    }
                }
            }
        },"""

fixed_section = """    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = { Text("لوحة تحكم المشرف") },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        IconButton(onClick = onNavigateToImport) {
                            Icon(androidx.compose.material.icons.Icons.Filled.UploadFile, contentDescription = "استيراد")
                        }
                    }
                )
                TabRow(selectedTabIndex = selectedTab) {
                    tabs.forEachIndexed { index, title ->
                        Tab(
                            selected = selectedTab == index,
                            onClick = { selectedTab = index },
                            text = { Text(title) }
                        )
                    }
                }
            }
        },"""

content = content.replace(broken_section, fixed_section)

# Also ensure onNavigateToImport is in the arguments properly!
content = content.replace("fun AdminDashboardScreen(\n        onBack: () -> Unit,\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n) {", 
"fun AdminDashboardScreen(\n    onBack: () -> Unit,\n    onNavigateToImport: () -> Unit = {},\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n) {")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
