import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "r") as f:
    content = f.read()

state_declaration = """
    var showLogoutDialog by remember { mutableStateOf(false) }
    var showAboutDialog by remember { mutableStateOf(false) }
"""

content = content.replace(
    'var showLogoutDialog by remember { mutableStateOf(false) }',
    state_declaration.strip()
)

# Weather button
content = content.replace(
    'onClick = { }',
    'onClick = { val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS); context.startActivity(intent) }',
    1 # First empty onClick is for Weather
)

# Notifications button
content = content.replace(
    'onClick = { }',
    'onClick = { android.widget.Toast.makeText(context, "خدمة الإشعارات ستكون متاحة قريباً", android.widget.Toast.LENGTH_SHORT).show() }',
    1
)

# About button
content = content.replace(
    'onClick = { }',
    'onClick = { showAboutDialog = true }',
    1
)

dialog_code = """
        if (showAboutDialog) {
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
"""

content = re.sub(r'    }\n}\s*@Composable', dialog_code + '\n@Composable', content)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "w") as f:
    f.write(content)
