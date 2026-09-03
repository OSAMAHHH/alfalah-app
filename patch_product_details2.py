import re
with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'fun ProductDetailsScreen(\n    productId: String,\n    onBack: () -> Unit,\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }',
    'fun ProductDetailsScreen(\n    productId: String,\n    onBack: () -> Unit,\n    onNavigateToCart: () -> Unit = {},\n    modifier: Modifier = Modifier,\n    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }'
)

content = content.replace(
    'IconButton(onClick = { /* Navigate to cart */ }',
    'IconButton(onClick = onNavigateToCart'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content)
