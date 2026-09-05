with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

# Replace conversations with chat in Bottom Navigation
content = content.replace('Pair("conversations", "المساعد") to Icons.Filled.Chat', 'Pair("chat?id=&initialQuery=", "المساعد") to Icons.Filled.Chat')

# Fix onNavigateToChat in MainScreen Home
content = content.replace('onNavigateToChat = { navController.navigate("conversations") }', 'onNavigateToChat = { navController.navigate("chat?id=&initialQuery=") }')

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()
    
# Wait, HomeScreen doesn't dictate the route, it just calls the lambda `onNavigateToChat()`. The lambda is in AppNavigation.kt.
# Let's double check if there's any direct route call.
