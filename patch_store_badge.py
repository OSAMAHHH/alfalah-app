with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()

badge_imports = """import androidx.compose.material3.*
import androidx.compose.runtime.*"""
new_badge_imports = """import androidx.compose.material3.*
import androidx.compose.runtime.*
import com.example.alfalah.data.model.CartItem"""
if "com.example.alfalah.data.model.CartItem" not in content:
    content = content.replace(badge_imports, new_badge_imports)

vars_block = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()"""
    
new_vars_block = """    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var cartItemsCount by remember { mutableStateOf(0) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()"""
if "cartItemsCount" not in content:
    content = content.replace(vars_block, new_vars_block)

load_data_block = """                if (result.isSuccess) {
                    products = result.getOrDefault(emptyList())
                } else {"""
new_load_data_block = """                if (result.isSuccess) {
                    products = result.getOrDefault(emptyList())
                    userServicesRepository.getCartItems().onSuccess { items ->
                        cartItemsCount = items.size
                    }
                } else {"""
if "getCartItems" not in content:
    content = content.replace(load_data_block, new_load_data_block)

top_bar_actions = """                actions = {
                    IconButton(onClick = onNavigateToCart) {
                        Icon(Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                    }
                }"""
new_top_bar_actions = """                actions = {
                    IconButton(onClick = onNavigateToCart) {
                        BadgedBox(badge = { if (cartItemsCount > 0) Badge { Text(cartItemsCount.toString()) } }) {
                            Icon(Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                        }
                    }
                }"""
if "BadgedBox" not in content:
    content = content.replace(top_bar_actions, new_top_bar_actions)

add_to_cart_block = """                                val result = userServicesRepository.addToCart(item)
                                if (result.isSuccess) Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()"""
new_add_to_cart_block = """                                val result = userServicesRepository.addToCart(item)
                                if (result.isSuccess) {
                                    cartItemsCount += 1
                                    Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()
                                }"""
if "cartItemsCount += 1" not in content:
    content = content.replace(add_to_cart_block, new_add_to_cart_block)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)
