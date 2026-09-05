import re
with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Fix hide bottom bar logic
old_hide = "val showBottomBar = items.any { it.first.first == currentDestination?.route }"
new_hide = """val showBottomBar = items.any { 
                val destRoute = currentDestination?.route ?: ""
                val itemRoute = it.first
                destRoute == itemRoute || (itemRoute.startsWith("chat") && destRoute.startsWith("chat"))
            }"""
content = content.replace(old_hide, new_hide)

# Fix selected logic
old_selected = "selected = currentDestination?.hierarchy?.any { it.route == route } == true,"
new_selected = """selected = currentDestination?.hierarchy?.any { 
                                val destRoute = it.route ?: ""
                                destRoute == route || (route.startsWith("chat") && destRoute.startsWith("chat"))
                            } == true,"""
content = content.replace(old_selected, new_selected)

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
