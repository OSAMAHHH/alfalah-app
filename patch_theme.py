import re
import os

# 1. Update Color.kt
color_file = "app/src/main/java/com/example/alfalah/ui/theme/Color.kt"
with open(color_file, "r") as f:
    color_content = f.read()

dark_colors = """
val PrimaryDark = Color(0xFF81C784)
val OnPrimaryDark = Color(0xFF00390A)
val PrimaryContainerDark = Color(0xFF005313)
val OnPrimaryContainerDark = Color(0xFFA5F2A9)
val SecondaryDark = Color(0xFFFFB74D)
val OnSecondaryDark = Color(0xFF4C2700)
val SecondaryContainerDark = Color(0xFF6B3A00)
val OnSecondaryContainerDark = Color(0xFFFFDCC1)
val BackgroundDark = Color(0xFF111412)
val OnBackgroundDark = Color(0xFFE1E3DF)
val SurfaceDark = Color(0xFF111412)
val OnSurfaceDark = Color(0xFFE1E3DF)
val SurfaceVariantDark = Color(0xFF434842)
val OnSurfaceVariantDark = Color(0xFFC3C8BF)
val OutlineDark = Color(0xFF8D938B)
val ErrorDark = Color(0xFFFFB4AB)
val OnErrorDark = Color(0xFF690005)
val ErrorContainerDark = Color(0xFF93000A)
val OnErrorContainerDark = Color(0xFFFFDAD6)
"""

if "PrimaryDark" not in color_content:
    with open(color_file, "w") as f:
        f.write(color_content + dark_colors)

# 2. Update Theme.kt
theme_file = "app/src/main/java/com/example/alfalah/ui/theme/Theme.kt"
with open(theme_file, "r") as f:
    theme_content = f.read()

dark_scheme = """private val DarkColorScheme = darkColorScheme(
    primary = PrimaryDark, onPrimary = OnPrimaryDark, primaryContainer = PrimaryContainerDark, onPrimaryContainer = OnPrimaryContainerDark,
    secondary = SecondaryDark, onSecondary = OnSecondaryDark, secondaryContainer = SecondaryContainerDark, onSecondaryContainer = OnSecondaryContainerDark,
    background = BackgroundDark, onBackground = OnBackgroundDark, surface = SurfaceDark, onSurface = OnSurfaceDark,
    surfaceVariant = SurfaceVariantDark, onSurfaceVariant = OnSurfaceVariantDark, error = ErrorDark, onError = OnErrorDark,
    errorContainer = ErrorContainerDark, onErrorContainer = OnErrorContainerDark, outline = OutlineDark
)
"""

if "DarkColorScheme" not in theme_content:
    theme_content = theme_content.replace("val AppShapes", dark_scheme + "\nval AppShapes")

    theme_content = theme_content.replace(
        "val colorScheme = LightColorScheme",
        "val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme"
    )
    theme_content = theme_content.replace(
        "WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = true",
        "WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme"
    )
    theme_content = theme_content.replace(
        "WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = true",
        "WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = !darkTheme"
    )

    with open(theme_file, "w") as f:
        f.write(theme_content)

# 3. Create ThemeManager.kt
os.makedirs("app/src/main/java/com/example/alfalah/utils", exist_ok=True)
theme_manager_file = "app/src/main/java/com/example/alfalah/utils/ThemeManager.kt"
theme_manager_content = """package com.example.alfalah.utils

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

object ThemeManager {
    private const val PREFS_NAME = "theme_prefs"
    private const val KEY_IS_DARK_MODE = "is_dark_mode"
    
    private val _isDarkMode = MutableStateFlow<Boolean?>(null)
    val isDarkMode: StateFlow<Boolean?> = _isDarkMode

    fun init(context: Context) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        if (prefs.contains(KEY_IS_DARK_MODE)) {
            _isDarkMode.value = prefs.getBoolean(KEY_IS_DARK_MODE, false)
        }
    }

    fun toggleTheme(context: Context, isDark: Boolean) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putBoolean(KEY_IS_DARK_MODE, isDark).apply()
        _isDarkMode.value = isDark
    }
}
"""
with open(theme_manager_file, "w") as f:
    f.write(theme_manager_content)

# 4. Update MainActivity.kt
main_activity_file = "app/src/main/java/com/example/alfalah/MainActivity.kt"
with open(main_activity_file, "r") as f:
    main_activity_content = f.read()

if "ThemeManager" not in main_activity_content:
    main_activity_content = main_activity_content.replace(
        "import com.example.alfalah.ui.theme.AlFalahTheme",
        "import com.example.alfalah.ui.theme.AlFalahTheme\nimport com.example.alfalah.utils.ThemeManager\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.getValue\nimport androidx.compose.foundation.isSystemInDarkTheme"
    )
    
    main_activity_content = main_activity_content.replace(
        "setContent {",
        "ThemeManager.init(applicationContext)\n        setContent {\n            val isDarkModeFlow by ThemeManager.isDarkMode.collectAsState()\n            val isSystemDark = isSystemInDarkTheme()\n            val isDark = isDarkModeFlow ?: isSystemDark"
    )
    
    main_activity_content = main_activity_content.replace(
        "AlFalahTheme {",
        "AlFalahTheme(darkTheme = isDark) {"
    )
    
    with open(main_activity_file, "w") as f:
        f.write(main_activity_content)

