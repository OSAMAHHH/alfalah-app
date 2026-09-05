package com.example.alfalah

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.example.alfalah.ui.navigation.AppNavigation
import com.example.alfalah.ui.theme.AlFalahTheme
import com.example.alfalah.utils.ThemeManager
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.foundation.isSystemInDarkTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        ThemeManager.init(applicationContext)
        setContent {
            val isDarkModeFlow by ThemeManager.isDarkMode.collectAsState()
            val isSystemDark = isSystemInDarkTheme()
            val isDark = isDarkModeFlow ?: isSystemDark
            AlFalahTheme(darkTheme = isDark) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppNavigation()
                }
            }
        }
    }
}
