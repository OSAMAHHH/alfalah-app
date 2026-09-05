import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CartScreen.kt", "r") as f:
    content = f.read()

# Fix loadCart to check auth
old_load_cart = """    fun loadCart() {
        scope.launch {
            val result = userRepo.getCartItems()
            if (result.isSuccess) {
                items = result.getOrDefault(emptyList())
            }
            isLoading = false
        }
    }"""
    
new_load_cart = """    fun loadCart() {
        scope.launch {
            if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser == null) {
                items = emptyList()
                isLoading = false
                return@launch
            }
            val result = userRepo.getCartItems()
            if (result.isSuccess) {
                items = result.getOrDefault(emptyList())
            }
            isLoading = false
        }
    }"""

content = content.replace(old_load_cart, new_load_cart)

# Fix bottomBar visibility to always show, but disable button if empty
old_bottom_bar = """            bottomBar = {
                if (items.isNotEmpty()) {
                    Surface("""
                    
new_bottom_bar = """            bottomBar = {
                if (true) {
                    Surface("""

old_button = """                            Button(
                                onClick = onCheckout,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp),
                                shape = RoundedCornerShape(12.dp),
                                enabled = !isUpdating
                            ) {"""

new_button = """                            Button(
                                onClick = onCheckout,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp),
                                shape = RoundedCornerShape(12.dp),
                                enabled = items.isNotEmpty() && !isUpdating
                            ) {"""

content = content.replace(old_bottom_bar, new_bottom_bar)
content = content.replace(old_button, new_button)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CartScreen.kt", "w") as f:
    f.write(content)
