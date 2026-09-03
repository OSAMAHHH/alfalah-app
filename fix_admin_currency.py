import re
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

# Fix the dropdown to include YER
old_dropdown = 'val currencies = listOf("SAR", "USD")'
new_dropdown = 'val currencies = listOf("YER", "SAR", "USD")'
content = content.replace(old_dropdown, new_dropdown)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
