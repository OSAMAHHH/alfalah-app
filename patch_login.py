import re

with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add a spacer and a divider
separator = """
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                    ) {
                        HorizontalDivider(modifier = Modifier.weight(1f), color = MaterialTheme.colorScheme.outlineVariant)
                        Text(
                            text = "أو",
                            modifier = Modifier.padding(horizontal = 16.dp),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        HorizontalDivider(modifier = Modifier.weight(1f), color = MaterialTheme.colorScheme.outlineVariant)
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // Google Login Button
"""

content = content.replace("                    }\n                    \n                    \n                    // Google Login Button", separator)

with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
