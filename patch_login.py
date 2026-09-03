import re

with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "r") as f:
    content = f.read()

# Add states for dialog
state_declaration = """
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    
    var showForgotPasswordDialog by remember { mutableStateOf(false) }
    var forgotPasswordEmail by remember { mutableStateOf("") }
    var isSendingResetEmail by remember { mutableStateOf(false) }
"""

content = content.replace(
    'var isLoading by remember { mutableStateOf(false) }\n    var errorMessage by remember { mutableStateOf<String?>(null) }',
    state_declaration.strip()
)

# Replace the onClick
content = content.replace(
    'onClick = { /* No function implemented in project */ }',
    'onClick = { showForgotPasswordDialog = true }'
)

# Add dialog at the end before closing braces
dialog_code = """
        if (showForgotPasswordDialog) {
            AlertDialog(
                onDismissRequest = { showForgotPasswordDialog = false },
                title = { Text("استعادة كلمة المرور") },
                text = {
                    Column {
                        Text("أدخل بريدك الإلكتروني وسنرسل لك رابطاً لإعادة تعيين كلمة المرور.")
                        Spacer(modifier = Modifier.height(16.dp))
                        OutlinedTextField(
                            value = forgotPasswordEmail,
                            onValueChange = { forgotPasswordEmail = it },
                            label = { Text("البريد الإلكتروني") },
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                },
                confirmButton = {
                    Button(
                        onClick = {
                            if (forgotPasswordEmail.isNotBlank()) {
                                isSendingResetEmail = true
                                scope.launch {
                                    val result = authRepository.resetPassword(forgotPasswordEmail)
                                    isSendingResetEmail = false
                                    showForgotPasswordDialog = false
                                    if (result.isSuccess) {
                                        android.widget.Toast.makeText(context, "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني.", android.widget.Toast.LENGTH_LONG).show()
                                    } else {
                                        android.widget.Toast.makeText(context, result.exceptionOrNull()?.message ?: "حدث خطأ.", android.widget.Toast.LENGTH_LONG).show()
                                    }
                                }
                            }
                        },
                        enabled = !isSendingResetEmail
                    ) {
                        if (isSendingResetEmail) {
                            CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary, strokeWidth = 2.dp)
                        } else {
                            Text("إرسال")
                        }
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showForgotPasswordDialog = false }) {
                        Text("إلغاء")
                    }
                }
            )
        }
    }
}
"""

content = re.sub(r'    }\n}\s*$', dialog_code, content)

with open("app/src/main/java/com/example/alfalah/ui/screens/auth/LoginScreen.kt", "w") as f:
    f.write(content)
