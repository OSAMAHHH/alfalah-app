import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'text = { Text("تطبيق الفلاحالإصدار 1.0.0تطبيق زراعي متكامل يهدف إلى مساعدة المزارعين من خلال توفير معلومات دقيقة حول المحاصيل، الآفات، والمنتجات الزراعية، بالإضافة إلى مساعد ذكي زراعي.',
    'text = { Text("تطبيق الفلاح\\nالإصدار 1.0.0\\nتطبيق زراعي متكامل يهدف إلى مساعدة المزارعين من خلال توفير معلومات دقيقة حول المحاصيل، الآفات، والمنتجات الزراعية، بالإضافة إلى مساعد ذكي زراعي.\\n\\nتطوير: فريق الفلاح") }',
)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "w") as f:
    f.write(content)
