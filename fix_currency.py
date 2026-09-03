import re

def fix_file(path):
    with open(path, "r") as f:
        content = f.read()
    
    if "import com.example.alfalah.utils.CurrencyUtils" not in content:
        content = content.replace("import com.example.alfalah.data.model.Product", "import com.example.alfalah.data.model.Product\nimport com.example.alfalah.utils.CurrencyUtils")
        
    old_currency = r'"\$\{product\??\.price\} \$\{if \(product\??\.currency\.isEmpty\(\) \|\| product\??\.currency == "\$" \|\| product\??\.currency == "SAR"\) "ر\.ي" else product\??\.currency\}"'
    new_currency = 'CurrencyUtils.formatPrice(product?.price ?: 0.0, product?.currency ?: "")'
    
    # StoreScreen uses product.price
    old_currency_store = r'"\$\{product\.price\} \$\{if \(product\.currency\.isEmpty\(\) \|\| product\.currency == "\$" \|\| product\.currency == "SAR"\) "ر\.ي" else product\.currency\}"'
    new_currency_store = 'CurrencyUtils.formatPrice(product.price, product.currency)'
    
    content = re.sub(old_currency, new_currency, content)
    content = re.sub(old_currency_store, new_currency_store, content)

    with open(path, "w") as f:
        f.write(content)

fix_file("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt")
fix_file("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt")

