import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

# Add AdminOrdersScreen tab
content = content.replace('val tabs = listOf("المنتجات", "المحاصيل", "المشاكل")', 'val tabs = listOf("المنتجات", "المحاصيل", "المشاكل", "الطلبات")')

# Render AdminOrdersScreen when tab is selected
admin_orders = """
                2 -> {
                    // Problems
"""

content = content.replace(
    '2 -> {',
    '3 -> {\n                    com.example.alfalah.ui.screens.admin.AdminOrdersScreen()\n                }\n                2 -> {'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
