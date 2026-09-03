import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Update showBottomBar
old_show = "val showBottomBar = currentRoute in listOf(Routes.HOME, Routes.STORE, Routes.CHAT, Routes.PROFILE)"
new_show = "val showBottomBar = currentRoute in listOf(Routes.HOME, Routes.STORE, Routes.CHAT, Routes.CHAT_ROUTE, Routes.PROFILE)"
content = content.replace(old_show, new_show)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
