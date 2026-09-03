import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

store_effect = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        val result = firestoreRepository.getProducts()
        if (result.isSuccess) products = result.getOrDefault(emptyList())
        isLoading = false
    }"""
store_effect_new = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    
    fun loadData() {
        isLoading = true
        errorMsg = null
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
            try {
                val result = firestoreRepository.getProducts()
                if (result.isSuccess) {
                    products = result.getOrDefault(emptyList())
                } else {
                    errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                }
            } catch (e: Exception) {
                errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
            } finally {
                isLoading = false
            }
        }
    }
    
    LaunchedEffect(Unit) {
        loadData()
    }"""
content = content.replace(store_effect, store_effect_new)

# Also add import kotlinx.coroutines.launch if missing. It might already be there or we can just use the scope.
# Oh, we need `import kotlinx.coroutines.launch` but we used `CoroutineScope(Dispatchers.Main).launch` which is fine.

store_empty = """        } else if (products.isEmpty()) {
            EmptyState(
                icon = Icons.Outlined.SearchOff,
                title = "المتجر فارغ",
                message = "لا تتوفر منتجات في الوقت الحالي، يرجى العودة لاحقاً.",
                modifier = Modifier.padding(padding)
            )
        } else {"""
store_empty_new = """        } else if (errorMsg != null) {
            Column(modifier = Modifier.fillMaxSize().padding(padding), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                EmptyState(
                    icon = Icons.Outlined.SearchOff,
                    title = "عذراً",
                    message = errorMsg!!,
                    modifier = Modifier.weight(1f)
                )
                Button(onClick = { loadData() }, modifier = Modifier.padding(bottom = 32.dp)) {
                    Text("إعادة المحاولة")
                }
            }
        } else if (products.isEmpty()) {
            EmptyState(
                icon = Icons.Outlined.SearchOff,
                title = "المتجر فارغ",
                message = "لا تتوفر منتجات في الوقت الحالي، يرجى العودة لاحقاً.",
                modifier = Modifier.padding(padding)
            )
        } else {"""
content = content.replace(store_empty, store_empty_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
