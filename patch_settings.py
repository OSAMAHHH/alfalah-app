import re

settings_file = "app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt"
with open(settings_file, "r") as f:
    settings_content = f.read()

# Add imports
if "import com.example.alfalah.utils.ThemeManager" not in settings_content:
    settings_content = settings_content.replace(
        "import androidx.compose.ui.unit.dp",
        "import androidx.compose.ui.unit.dp\nimport com.example.alfalah.utils.ThemeManager\nimport androidx.compose.foundation.isSystemInDarkTheme\nimport androidx.compose.material.icons.filled.DarkMode"
    )

# Add SettingsSwitchItem Composable
if "fun SettingsSwitchItem" not in settings_content:
    settings_content += """
@Composable
fun SettingsSwitchItem(
    icon: ImageVector,
    title: String,
    subtitle: String,
    isChecked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onCheckedChange(!isChecked) },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Switch(
                checked = isChecked,
                onCheckedChange = onCheckedChange,
                colors = SwitchDefaults.colors(checkedThumbColor = MaterialTheme.colorScheme.primary, checkedTrackColor = MaterialTheme.colorScheme.primaryContainer)
            )
        }
    }
}
"""

# Insert the toggle item in SettingsScreen
if "val isDarkModeFlow" not in settings_content:
    settings_content = settings_content.replace(
        "val context = LocalContext.current",
        "val context = LocalContext.current\n    val isDarkModeFlow by ThemeManager.isDarkMode.collectAsState()\n    val isSystemDark = isSystemInDarkTheme()\n    val isDark = isDarkModeFlow ?: isSystemDark"
    )

    toggle_code = """
                SettingsSwitchItem(
                    icon = Icons.Filled.DarkMode,
                    title = "الوضع الليلي",
                    subtitle = "تفعيل المظهر الداكن لإراحة العين",
                    isChecked = isDark,
                    onCheckedChange = { ThemeManager.toggleTheme(context, it) }
                )
                """
    
    settings_content = settings_content.replace(
        "verticalArrangement = Arrangement.spacedBy(16.dp)\n            ) {",
        "verticalArrangement = Arrangement.spacedBy(16.dp)\n            ) {\n" + toggle_code
    )

with open(settings_file, "w") as f:
    f.write(settings_content)
