import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

store_old = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        val result = firestoreRepository.getProducts()
        if (result.isSuccess) products = result.getOrDefault(emptyList())
        isLoading = false
    }"""
store_new = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
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
content = content.replace(store_old, store_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
