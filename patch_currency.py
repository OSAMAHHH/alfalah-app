import re

files_to_patch = [
    "app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt",
    "app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt"
]

for file_path in files_to_patch:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We want to intercept ${product.price} ${product.currency} and display YER appropriately
    
    # In Kotlin, we can replace:
    # "${product.price} ${product.currency}"
    # with:
    # "${product.price} ${if (product.currency.isEmpty() || product.currency == \"$\" || product.currency == \"SAR\") \"ر.ي\" else product.currency}"
    
    new_currency = '${product.price} ${if (product.currency.isEmpty() || product.currency == "$" || product.currency == "SAR") "ر.ي" else product.currency}'
    
    content = content.replace('${product.price} ${product.currency}', new_currency)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Currency patched.")
