import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the Scaffold body completely
# Scaffold( ... ) { padding -> ... }

# Find the start of { padding ->
start_idx = content.find(") { padding ->")
end_idx = content.find("}\n\n@Composable\nfun CropCard(crop: Crop)")

if start_idx != -1 and end_idx != -1:
    new_body = """) { padding ->
        if (isLoading) {
            com.example.alfalah.ui.components.LoadingState(modifier = Modifier.padding(padding))
        } else if (items.isEmpty()) {
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
                    message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                    modifier = Modifier.padding(padding)
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(items.size) { index ->
                    val item = items[index]
                    when (item) {
                        is Crop -> CropCard(item as Crop)
                        is AgriculturalProblem -> ProblemCard(item as AgriculturalProblem)
                    }
                    
                    if (index == items.size - 1 && hasMore && !isLoadingMore) {
                        LaunchedEffect(index) {
                            loadData(true)
                        }
                    }
                }
                
                if (isLoadingMore) {
                    item {
                        Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(modifier = Modifier.size(32.dp), color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }
        }
    """
    content = content[:start_idx] + new_body + content[end_idx:]

    with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
        f.write(content)
