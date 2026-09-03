import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the GuideScreen signature
sig_old = """@Composable
fun GuideScreen(
    category: String,
    onBack: () -> Unit,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {"""
sig_new = """@Composable
fun GuideScreen(
    category: String,
    onBack: () -> Unit,
    onNavigateToCrop: (String) -> Unit = {},
    onNavigateToProblem: (String) -> Unit = {},
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {"""
content = content.replace(sig_old, sig_new)

# Add imports for search and filters
imports = """
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
"""
content = content.replace("import androidx.compose.animation.AnimatedVisibility", imports + "\nimport androidx.compose.animation.AnimatedVisibility")

# In GuideScreen body, add search and filter states
state_old = """    var items by remember { mutableStateOf<List<Any>>(emptyList()) }
    var lastDoc by remember { mutableStateOf<com.google.firebase.firestore.DocumentSnapshot?>(null) }"""
state_new = """    var items by remember { mutableStateOf<List<Any>>(emptyList()) }
    var lastDoc by remember { mutableStateOf<com.google.firebase.firestore.DocumentSnapshot?>(null) }
    var searchQuery by remember { mutableStateOf("") }
    var selectedFilter by remember { mutableStateOf("الكل") }"""
content = content.replace(state_old, state_new)

# Modify LoadData to fetch everything if we are going to do local search properly, 
# or just keep pagination and filter what we have.
# The prompt: "تأكد من استمرار عمل Pagination." and "لا تجعل البحث يعيد تحميل Firestore عند كل حرف. يجب البحث في البيانات المحملة بالفعل."
# We will just filter the loaded items locally.

filter_logic = """
    val filteredItems = remember(items, searchQuery, selectedFilter) {
        items.filter { item ->
            val matchesSearch = if (searchQuery.isBlank()) true else {
                when (item) {
                    is Crop -> {
                        item.name.contains(searchQuery, ignoreCase = true) ||
                        item.synonyms.any { it.contains(searchQuery, ignoreCase = true) } ||
                        item.description.contains(searchQuery, ignoreCase = true)
                    }
                    is AgriculturalProblem -> {
                        item.name.contains(searchQuery, ignoreCase = true) ||
                        item.synonyms.any { it.contains(searchQuery, ignoreCase = true) } ||
                        item.symptoms.any { it.contains(searchQuery, ignoreCase = true) }
                    }
                    else -> false
                }
            }
            
            val matchesFilter = if (selectedFilter == "الكل") true else {
                when (item) {
                    is AgriculturalProblem -> item.type == selectedFilter
                    else -> true
                }
            }
            
            matchesSearch && matchesFilter
        }
    }
    
    val problemFilters = listOf("الكل", "الأمراض", "الآفات", "نقص العناصر الغذائية", "مشاكل أخرى")
"""
content = content.replace("    val title = when (category) {", filter_logic + "\n    val title = when (category) {")

# Update LazyColumn items to use filteredItems
lazy_old = """            LazyColumn(
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
                }
                
                if (hasMore) {
                    item {
                        if (isLoadingMore) {
                            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                                CircularProgressIndicator()
                            }
                        } else {
                            LaunchedEffect(Unit) {
                                loadData(true)
                            }
                        }
                    }
                }
            }"""

lazy_new = """            Column(modifier = Modifier.fillMaxSize().padding(padding)) {
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
                        }
                        
                        if (hasMore) {
                            item {
                                if (isLoadingMore) {
                                    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                                        CircularProgressIndicator()
                                    }
                                } else {
                                    LaunchedEffect(filteredItems.size) {
                                        // Auto load more when reaching bottom
                                        loadData(true)
                                    }
                                }
                            }
                        }
                    }
                }
            }"""

content = content.replace(lazy_old, lazy_new)

# Now we need to modify CropCard and ProblemCard to be simpler cards that trigger onClick.
crop_card_old = """@Composable
fun CropCard(crop: Crop, userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }) {"""
crop_card_new = """@Composable
fun CropCard(
    crop: Crop, 
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    onClick: () -> Unit = {}
) {"""
content = content.replace(crop_card_old, crop_card_new)

problem_card_old = """@Composable
fun ProblemCard(problem: AgriculturalProblem, userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }) {"""
problem_card_new = """@Composable
fun ProblemCard(
    problem: AgriculturalProblem, 
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    onClick: () -> Unit = {}
) {"""
content = content.replace(problem_card_old, problem_card_new)

# Update their modifier to use the provided onClick instead of expanding.
# We'll just replace the expanded logic with onClick.
crop_mod_old = "modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }"
crop_mod_new = "modifier = Modifier.fillMaxWidth().clickable { onClick() }"
content = content.replace(crop_mod_old, crop_mod_new)

problem_mod_old = "modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }"
problem_mod_new = "modifier = Modifier.fillMaxWidth().clickable { onClick() }"
content = content.replace(problem_mod_old, problem_mod_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
