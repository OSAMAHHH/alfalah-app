with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "r") as f:
    content = f.read()

bad = """                    Row(
                        verticalAlignment = Alignment.CenterVertically,"""

good = """                    Spacer(modifier = Modifier.height(12.dp))
                    TextButton(
                        onClick = onLoginSuccess,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("الدخول كزائر", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.primary)
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    Row(
                        verticalAlignment = Alignment.CenterVertically,"""

content = content.replace(bad, good)

with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "w") as f:
    f.write(content)
