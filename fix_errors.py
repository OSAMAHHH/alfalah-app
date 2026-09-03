import re

# Fix HomeScreen.kt
with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r", encoding="utf-8") as f:
    home = f.read()

home = home.replace("val cropIdsRes = userServicesRepository.getMyCrops()\n                if (cropIdsRes.isSuccess) {\n                    val ids = cropIdsRes.getOrNull()?.map { it.itemId } ?: emptyList()", "val cropsList = userServicesRepository.getMyCrops()\n                if (true) {\n                    val ids = cropsList.map { it.cropId }")
home = home.replace("val res = firestoreRepository.getProductsPaginated(5, null)\n            if (res.isSuccess) {\n                featuredProducts = res.getOrNull()?.first ?: emptyList()\n            }", "val res = firestoreRepository.getProducts()\n            if (res.isSuccess) {\n                featuredProducts = res.getOrDefault(emptyList()).take(5)\n            }")

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w", encoding="utf-8") as f:
    f.write(home)

# Fix MyCropsScreen.kt
with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "r", encoding="utf-8") as f:
    my_crops = f.read()

mc_old = """    LaunchedEffect(Unit) {
        val res = userServicesRepository.getMyCrops()
        if (res.isSuccess) {
            val cropsData = res.getOrDefault(emptyList())
            myCrops = cropsData
            
            // Fetch crop details
            val fullCrops = mutableListOf<Crop>()
            for (myCrop in cropsData) {
                val cres = firestoreRepository.getCropById(myCrop.cropId) 
                cres.getOrNull()?.let { fullCrops.add(it) }
            }
            loadedCrops = fullCrops
        }
        isLoading = false
    }"""
mc_new = """    LaunchedEffect(Unit) {
        try {
            val cropsData = userServicesRepository.getMyCrops()
            myCrops = cropsData
            
            // Fetch crop details
            val fullCrops = mutableListOf<Crop>()
            for (myCrop in cropsData) {
                val cres = firestoreRepository.getCropById(myCrop.cropId) 
                cres.getOrNull()?.let { fullCrops.add(it) }
            }
            loadedCrops = fullCrops
        } catch (e: Exception) {}
        isLoading = false
    }"""
my_crops = my_crops.replace(mc_old, mc_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "w", encoding="utf-8") as f:
    f.write(my_crops)

# Fix StoreScreen.kt
with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r", encoding="utf-8") as f:
    store = f.read()

store_old_effect = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        val result = firestoreRepository.getProducts()
        if (result.isSuccess) products = result.getOrDefault(emptyList())
        isLoading = false
    }"""
store_new_effect = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    
    val scope = rememberCoroutineScope()
    fun loadData() {
        isLoading = true
        errorMsg = null
        scope.launch {
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
store = store.replace(store_old_effect, store_new_effect)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w", encoding="utf-8") as f:
    f.write(store)

