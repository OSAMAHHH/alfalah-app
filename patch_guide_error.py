import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure EmptyState uses errorMsg
old_msg = 'message = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."'
new_msg = 'message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."'

content = content.replace(old_msg, new_msg)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
