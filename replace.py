import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

new_dialog = open("replace_product_dialog.kt", "r").read()

pattern = re.compile(r'fun ProductDialog\(.*?shape = RoundedCornerShape\(24\.dp\)\n    \)\n}', re.DOTALL)
content = re.sub(pattern, new_dialog, content, count=1)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
