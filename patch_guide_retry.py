import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

empty_old = """            } else {
                com.example.alfalah.ui.components.EmptyState(
                    icon = Icons.Filled.Eco,
                    title = "لا توجد بيانات",
                    message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                    modifier = Modifier.padding(padding)
                )
            }"""
            
empty_new = """            } else {
                Column(modifier = Modifier.fillMaxSize().padding(padding), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                    com.example.alfalah.ui.components.EmptyState(
                        icon = Icons.Filled.Eco,
                        title = "لا توجد بيانات",
                        message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                        modifier = Modifier.weight(1f)
                    )
                    if (errorMsg != null) {
                        Button(onClick = { loadData(false) }, modifier = Modifier.padding(bottom = 32.dp)) {
                            Text("إعادة المحاولة")
                        }
                    }
                }
            }"""
content = content.replace(empty_old, empty_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
