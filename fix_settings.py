import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "r") as f:
    content = f.read()

# Fix the broken text in the file.
# First, let's just find the broken part and replace it.
start_str = "        if (showAboutDialog) {"
end_str = "}@Composable"

match = re.search(r'        if \(showAboutDialog\) \{.*?\n\}\n@Composable', content, flags=re.DOTALL)
if match:
    content = content[:match.start()] + """        if (showAboutDialog) {
            AlertDialog(
                onDismissRequest = { showAboutDialog = false },
                title = { Text("حول التطبيق") },
                text = { Text("تطبيق الفلاح\\nالإصدار 1.0.0\\nتطبيق زراعي متكامل يهدف إلى مساعدة المزارعين من خلال توفير معلومات دقيقة حول المحاصيل، الآفات، والمنتجات الزراعية، بالإضافة إلى مساعد ذكي زراعي.\\n\\nتطوير: فريق الفلاح") },
                confirmButton = {
                    Button(onClick = { showAboutDialog = false }) {
                        Text("موافق")
                    }
                }
            )
        }
    }
}
@Composable""" + content[match.end():]

# Fix missing import for AlertDialog? No, it's already there.

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "w") as f:
    f.write(content)
