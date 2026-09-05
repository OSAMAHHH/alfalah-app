with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

content = content.replace('listOf("SAR", "USD", "EGP", "AED")', 'listOf("YER", "SAR", "USD")')

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
