import re

def fix_store(path):
    with open(path, "r") as f:
        content = f.read()

    # StoreScreen
    # Replace the empty onClick in the cart icon
    content = content.replace(
        'onClick = { /* Add to cart */ }',
        'onClick = { onAddToCart(product) }'
    )
    
    # StoreScreen parameters
    content = content.replace(
        'fun StoreScreen(\n    onNavigateToProduct: (String) -> Unit,\n    onBack: () -> Unit,\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n)',
        'fun StoreScreen(\n    onNavigateToProduct: (String) -> Unit,\n    onBack: () -> Unit,\n    onNavigateToCart: () -> Unit,\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },\n    userServicesRepository: com.example.alfalah.data.repository.UserServicesRepository = remember { com.example.alfalah.data.repository.UserServicesRepository() }\n)'
    )
    
    # Add cart button to TopAppBar
    appbar = """
                TopAppBar(
                    title = { Text("المتجر الزراعي", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        IconButton(onClick = onNavigateToCart) {
                            Icon(androidx.compose.material.icons.Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                        }
                    }
                )"""
    
    # Replace topbar
    content = re.sub(r'TopAppBar\([\s\S]*?Icon\(Icons.AutoMirrored.Outlined.ArrowBack[^\)]*\)[\s\S]*?\}[\s\S]*?\}[\s\S]*?\)', appbar.strip(), content)

    # Implement onAddToCart
    content = content.replace(
        'val firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }',
        'val firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }\n    val userServicesRepository = remember { com.example.alfalah.data.repository.UserServicesRepository() }\n    val scope = rememberCoroutineScope()\n    val context = androidx.compose.ui.platform.LocalContext.current'
    )
    
    # In StoreScreen, add onAddToCart lambda for ProductCard
    content = content.replace(
        'ProductCard(product = product, onClick = { onNavigateToProduct(product.id) })',
        'ProductCard(product = product, onClick = { onNavigateToProduct(product.id) }, onAddToCart = { p ->\n                                scope.launch {\n                                    val item = com.example.alfalah.data.model.CartItem(productId = p.id, name = p.name, price = p.price, currency = p.currency.ifEmpty{"YER"}, imageUrl = p.imageUrl, quantity = 1)\n                                    val result = userServicesRepository.addToCart(item)\n                                    if(result.isSuccess) android.widget.Toast.makeText(context, "تمت الإضافة للسلة", android.widget.Toast.LENGTH_SHORT).show()\n                                    else android.widget.Toast.makeText(context, "حدث خطأ", android.widget.Toast.LENGTH_SHORT).show()\n                                }\n                            })'
    )
    
    content = content.replace(
        'fun ProductCard(product: Product, onClick: () -> Unit) {',
        'fun ProductCard(product: Product, onClick: () -> Unit, onAddToCart: (Product) -> Unit) {'
    )
    
    with open(path, "w") as f:
        f.write(content)

fix_store("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt")
