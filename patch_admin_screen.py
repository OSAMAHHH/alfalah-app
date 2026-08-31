import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

# Add parameter
content = content.replace("fun AdminDashboardScreen(onBack: () -> Unit) {", "fun AdminDashboardScreen(onBack: () -> Unit, onNavigateToImport: () -> Unit = {}) {")

# Add button in the Column. Let's look for:
#                 horizontalArrangement = Arrangement.spacedBy(16.dp)
#             ) {
#                 Tab(
# We will just add it below the TabRow, or at the top of the content.
# Let's just find the first TabRow and put a button before it.
# Actually, wait, let's put it in the TopAppBar actions!
#                 actions = {
#                    IconButton(onClick = onNavigateToImport) {
#                        Icon(Icons.Filled.UploadFile, contentDescription = "استيراد")
#                    }
#                 }

topbar_pattern = r'TopAppBar\(\s*title = \{ Text\("لوحة تحكم المشرف"\) \},\s*navigationIcon = \{[^\}]+\}[^\}]+\}'
# wait, there's a navigationIcon:
#                 navigationIcon = {
#                    IconButton(onClick = onBack) {
#                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "رجوع")
#                    }
#                }

replacement = """TopAppBar(
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
            )"""

content = re.sub(r'TopAppBar\([\s\S]*?navigationIcon = \{[\s\S]*?\}\s*?\n\s*\)', replacement, content)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
