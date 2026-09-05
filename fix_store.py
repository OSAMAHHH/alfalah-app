import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()

# Fix cartItemsCount initialization and refresh.
# Replace the loadData function and LaunchedEffect.
old_loadData = """    fun loadData() {
        isLoading = true
        errorMsg = null
        scope.launch {
            try {
                val result = firestoreRepository.getProducts()
                if (result.isSuccess) {
                    products = result.getOrDefault(emptyList())
                    userServicesRepository.getCartItems().onSuccess { items ->
                        cartItemsCount = items.size
                    }
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

new_loadData = """    fun loadData() {
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
    
    fun refreshCart() {
        scope.launch {
            if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) {
                userServicesRepository.getCartItems().onSuccess { items ->
                    cartItemsCount = items.size
                }
            }
        }
    }

    LaunchedEffect(Unit) {
        loadData()
    }
    
    // Refresh cart count every time screen becomes active (or just rely on local state updates)
    androidx.compose.runtime.DisposableEffect(androidx.lifecycle.compose.LocalLifecycleOwner.current) {
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->
            if (event == androidx.lifecycle.Lifecycle.Event.ON_RESUME) {
                refreshCart()
            }
        }
        val lifecycle = androidx.lifecycle.compose.LocalLifecycleOwner.current.lifecycle
        lifecycle.addObserver(observer)
        onDispose {
            lifecycle.removeObserver(observer)
        }
    }"""

if "fun refreshCart" not in content:
    content = content.replace(old_loadData, new_loadData)

# Fix onAddToCart for Guest users
old_add_to_cart = """                        onAddToCart = { p ->
                            scope.launch {
                                val item = CartItem(productId = p.id, name = p.name, price = p.price, currency = p.currency.ifEmpty { "YER" }, imageUrl = p.imageUrl, quantity = 1)
                                val result = userServicesRepository.addToCart(item)
                                if (result.isSuccess) {
                                    cartItemsCount += 1
                                    Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()
                                }
                                else Toast.makeText(context, result.exceptionOrNull()?.message ?: "حدث خطأ غير معروف", Toast.LENGTH_LONG).show()
                            }
                        }"""
                        
new_add_to_cart = """                        onAddToCart = { p ->
                            scope.launch {
                                if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser == null) {
                                    Toast.makeText(context, "الرجاء تسجيل الدخول أولاً لإضافة منتجات", Toast.LENGTH_LONG).show()
                                    return@launch
                                }
                                val item = CartItem(productId = p.id, name = p.name, price = p.price, currency = p.currency.ifEmpty { "YER" }, imageUrl = p.imageUrl, quantity = 1)
                                val result = userServicesRepository.addToCart(item)
                                if (result.isSuccess) {
                                    cartItemsCount += 1
                                    Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()
                                }
                                else Toast.makeText(context, result.exceptionOrNull()?.message ?: "حدث خطأ غير معروف", Toast.LENGTH_LONG).show()
                            }
                        }"""

content = content.replace(old_add_to_cart, new_add_to_cart)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)

