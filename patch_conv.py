import re
with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ConversationsScreen.kt", "r") as f:
    content = f.read()

bad = """    var conversations by remember { mutableStateOf<List<Conversation>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }"""

good = """    var conversations by remember { mutableStateOf<List<Conversation>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    
    val currentUser = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
    if (currentUser == null) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("المساعد الزراعي", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier.fillMaxSize().padding(padding).padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(Icons.Filled.Chat, contentDescription = null, modifier = Modifier.size(72.dp), tint = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(16.dp))
                Text("يرجى تسجيل الدخول أولاً", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                Spacer(modifier = Modifier.height(8.dp))
                Text("تحتاج إلى تسجيل الدخول لاستخدام المساعد الزراعي الذكي.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        return
    }"""

content = content.replace(bad, good)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ConversationsScreen.kt", "w") as f:
    f.write(content)
