import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace variables and LaunchedEffect in GuideScreen
old_variables = """    var isLoading by remember { mutableStateOf(true) }
    var items by remember { mutableStateOf<List<Any>>(emptyList()) }"""

new_variables = """    var isLoading by remember { mutableStateOf(true) }
    var items by remember { mutableStateOf<List<Any>>(emptyList()) }
    var lastDoc by remember { mutableStateOf<com.google.firebase.firestore.DocumentSnapshot?>(null) }
    var hasMore by remember { mutableStateOf(true) }
    var isLoadingMore by remember { mutableStateOf(false) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
"""
content = content.replace(old_variables, new_variables)

old_launched_effect = """    LaunchedEffect(category) {
        isLoading = true
        when (category) {
            "crops" -> {
                val res = firestoreRepository.getCrops()
                items = res.getOrDefault(emptyList())
            }
            "pests" -> {
                val res = firestoreRepository.getProblems()
                items = res.getOrDefault(emptyList())
            }
            "irrigation" -> {
                items = emptyList()
            }
        }
        isLoading = false
    }"""

new_launched_effect = """    fun loadData(isLoadMore: Boolean = false) {
        if (!hasMore && isLoadMore) return
        if (isLoadMore) isLoadingMore = true else isLoading = true
        
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
            try {
                when (category) {
                    "crops" -> {
                        val res = firestoreRepository.getCropsPaginated(15, if (isLoadMore) lastDoc else null)
                        if (res.isSuccess) {
                            val (newItems, nextDoc) = res.getOrThrow()
                            items = if (isLoadMore) items + newItems else newItems
                            lastDoc = nextDoc
                            hasMore = nextDoc != null
                            errorMsg = null
                        } else {
                            if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                        }
                    }
                    "pests" -> {
                        val res = firestoreRepository.getProblemsPaginated(15, if (isLoadMore) lastDoc else null)
                        if (res.isSuccess) {
                            val (newItems, nextDoc) = res.getOrThrow()
                            items = if (isLoadMore) items + newItems else newItems
                            lastDoc = nextDoc
                            hasMore = nextDoc != null
                            errorMsg = null
                        } else {
                            if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                        }
                    }
                    "irrigation" -> {
                        items = emptyList()
                        hasMore = false
                    }
                }
            } catch (e: Exception) {
                if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
            } finally {
                if (isLoadMore) isLoadingMore = false else isLoading = false
            }
        }
    }

    LaunchedEffect(category) {
        items = emptyList()
        lastDoc = null
        hasMore = true
        loadData(false)
    }
"""
content = content.replace(old_launched_effect, new_launched_effect)

# Now, add loading more trigger in LazyColumn
old_lazy = """            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(items) { item ->
                    when (item) {
                        is Crop -> CropCard(item)
                        is AgriculturalProblem -> ProblemCard(item)
                    }
                }
            }"""

new_lazy = """            LazyColumn(
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
            }"""
content = content.replace(old_lazy, new_lazy)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
