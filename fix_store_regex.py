import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace variables block
pattern = r"var products by remember \{ mutableStateOf<List<Product>>\(emptyList\(\)\) \}\s*var isLoading by remember \{ mutableStateOf\(true\) \}\s*LaunchedEffect\(Unit\) \{\s*val result = firestoreRepository\.getProducts\(\)\s*if \(result\.isSuccess\) products = result\.getOrDefault\(emptyList\(\)\)\s*isLoading = false\s*\}"

replacement = """var products by remember { mutableStateOf<List<Product>>(emptyList()) }
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

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
