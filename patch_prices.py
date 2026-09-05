import re

files_to_patch = [
    "app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt",
    "app/src/main/java/com/example/alfalah/ui/screens/guide/ProblemDetailsScreen.kt",
    "app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt",
    "app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt",
]

for filepath in files_to_patch:
    with open(filepath, "r") as f:
        content = f.read()

    # ChatScreen.kt
    content = content.replace('Text("${product.price} ر.ي",', 'Text(com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency),')
    
    # ProblemDetailsScreen.kt
    content = content.replace('Text("${product.price} ${product.currency}",', 'Text(com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency),')

    # AdminDashboardScreen.kt
    content = content.replace('"السعر: ${product.price} ر.س"', '"السعر: " + com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency)')
    content = content.replace('"السعر: ${product.price} ${product.currency}"', '"السعر: " + com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency)')

    # HomeScreen.kt
    content = content.replace('Text("${product.price} ${product.currency}",', 'Text(com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency),')

    with open(filepath, "w") as f:
        f.write(content)
