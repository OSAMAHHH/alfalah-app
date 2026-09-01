import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the simple Box with CircularProgressIndicator to LoadingState
loading_replacement = """        if (isLoading) {
            com.example.alfalah.ui.components.LoadingState(modifier = Modifier.padding(padding))
"""
content = re.sub(r'\s*if \(isLoading\) \{\s*Box.*?CircularProgressIndicator\(\)\s*\}\s*\}', '\n' + loading_replacement, content, flags=re.DOTALL)

# Replace the empty Box with EmptyState
empty_replacement = """        } else if (items.isEmpty()) {
            if (category == "irrigation") {
                com.example.alfalah.ui.components.EmptyState(
                    icon = Icons.Filled.WaterDrop,
                    title = "قريباً",
                    message = "سيتم إضافة دليل الري قريباً",
                    modifier = Modifier.padding(padding)
                )
            } else {
                com.example.alfalah.ui.components.EmptyState(
                    icon = Icons.Filled.Eco,
                    title = "لا توجد بيانات",
                    message = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                    modifier = Modifier.padding(padding)
                )
            }
"""
content = re.sub(r'\s*\} else if \(items.isEmpty\(\)\) \{\s*Box.*?Text\(.*?\}\s*\}', '\n' + empty_replacement, content, flags=re.DOTALL)


with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
