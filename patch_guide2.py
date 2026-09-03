import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the Scaffold body completely
scaffold_body_pattern = re.compile(r'    \) \{ padding ->\n        if \(isLoading\).*?^\}\n\n@Composable\nfun CropCard', re.MULTILINE | re.DOTALL)

new_scaffold_body = """    ) { padding ->
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
            Column(modifier = Modifier.fillMaxSize().padding(padding)) {
                // Search Bar
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                    placeholder = { Text("ابحث هنا...") },
                    leadingIcon = { Icon(Icons.Filled.Search, contentDescription = "بحث") },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Filled.Clear, contentDescription = "مسح البحث")
                            }
                        }
                    },
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surface,
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    ),
                    singleLine = true
                )
                
                // Filters
                if (category == "pests") {
                    LazyRow(
                        modifier = Modifier.fillMaxWidth(),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(problemFilters) { filter ->
                            FilterChip(
                                selected = selectedFilter == filter,
                                onClick = { selectedFilter = filter },
                                label = { Text(filter) }
                            )
                        }
                    }
                }
                
                if (filteredItems.isEmpty() && !isLoading) {
                    Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("لم نجد نتائج مطابقة", style = MaterialTheme.typography.titleMedium)
                            if (hasMore) {
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { loadData(true) }) {
                                    Text("تحميل المزيد من البيانات")
                                }
                            }
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.weight(1f).fillMaxWidth(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(filteredItems.size) { index ->
                            val item = filteredItems[index]
                            when (item) {
                                is Crop -> CropCard(item, onClick = { onNavigateToCrop(item.id) })
                                is AgriculturalProblem -> ProblemCard(item, onClick = { onNavigateToProblem(item.id) })
                            }
                            
                            // Auto load more when reaching bottom of original items
                            if (index == filteredItems.size - 1 && hasMore && !isLoadingMore) {
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
            }
        }
    }
}

@Composable
fun CropCard"""

new_content = scaffold_body_pattern.sub(new_scaffold_body, content)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(new_content)
