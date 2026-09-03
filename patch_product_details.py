import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content = f.read()

# Make onAddToCart functional
content = content.replace(
    'Button(\n                            onClick = { /* Add to cart */ },',
    'Button(\n                            onClick = { scope.launch {\n                                val item = com.example.alfalah.data.model.CartItem(productId = product?.id ?: "", name = product?.name ?: "", price = product?.price ?: 0.0, currency = product?.currency?.ifEmpty{"YER"} ?: "YER", imageUrl = product?.imageUrl ?: "", quantity = 1)\n                                val result = userServicesRepository.addToCart(item)\n                                if(result.isSuccess) Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()\n                                else Toast.makeText(context, "حدث خطأ", Toast.LENGTH_SHORT).show()\n                            } },'
)

# And add the cart icon to the top bar
appbar = """
                TopAppBar(
                    title = { Text("") },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent),
                    navigationIcon = {
                        IconButton(onClick = onBack, modifier = Modifier.background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f), androidx.compose.foundation.shape.CircleShape)) {
                            Icon(androidx.compose.material.icons.Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        IconButton(onClick = { /* Navigate to cart */ }, modifier = Modifier.background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f), androidx.compose.foundation.shape.CircleShape)) {
                            Icon(androidx.compose.material.icons.Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                        }
                    }
                )"""

content = re.sub(r'TopAppBar\([\s\S]*?Icon\(Icons.AutoMirrored.Outlined.ArrowBack[^\)]*\)[\s\S]*?\}[\s\S]*?\}[\s\S]*?\)', appbar.strip(), content)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content)
