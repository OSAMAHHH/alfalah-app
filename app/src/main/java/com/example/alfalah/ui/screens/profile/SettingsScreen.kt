package com.example.alfalah.ui.screens.profile

import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Logout
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Cloud
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.utils.ThemeManager
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material.icons.filled.DarkMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBack: () -> Unit,
    onLogout: () -> Unit,
    onNavigateToMyOrders: () -> Unit = {}
) {
    var showLogoutDialog by remember { mutableStateOf(false) }
    var showAboutDialog by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val isDarkModeFlow by ThemeManager.isDarkMode.collectAsState()
    val isSystemDark = isSystemInDarkTheme()
    val isDark = isDarkModeFlow ?: isSystemDark
    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("الإعدادات", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            }
        ) { paddingValues ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {

                SettingsSwitchItem(
                    icon = Icons.Filled.DarkMode,
                    title = "الوضع الليلي",
                    subtitle = "تفعيل المظهر الداكن لإراحة العين",
                    isChecked = isDark,
                    onCheckedChange = { ThemeManager.toggleTheme(context, it) }
                )
                
                SettingsItem(
                    icon = Icons.Filled.LocationOn,
                    title = "الموقع الجغرافي",
                    subtitle = "انتقل لإعدادات التطبيق لتفعيل/إلغاء إذن الموقع",
                    onClick = {
                        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                            data = Uri.fromParts("package", context.packageName, null)
                        }
                        context.startActivity(intent)
                    }
                )
                
                SettingsItem(
                    icon = Icons.Filled.Cloud,
                    title = "الطقس",
                    subtitle = "تعتمد بيانات الطقس على موقع الهاتف الحالي",
                    onClick = { val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS); context.startActivity(intent) }
                )
                
                SettingsItem(
                    icon = Icons.Filled.Notifications,
                    title = "الإشعارات",
                    subtitle = "قريباً - سيتم توفير إشعارات بالري والتسميد",
                    onClick = { android.widget.Toast.makeText(context, "خدمة الإشعارات ستكون متاحة قريباً", android.widget.Toast.LENGTH_SHORT).show() }
                )
                
                SettingsItem(
                    icon = androidx.compose.material.icons.Icons.Filled.List,
                    title = "طلباتي",
                    subtitle = "تتبع حالة طلباتك من المتجر الزراعي",
                    onClick = onNavigateToMyOrders
                )
                
                SettingsItem(
                    icon = Icons.Filled.Person,
                    title = "الحساب",
                    subtitle = "عرض معلومات الملف الشخصي",
                    onClick = onBack
                )
                
                SettingsItem(
                    icon = Icons.Filled.Info,
                    title = "حول التطبيق",
                    subtitle = "تطبيق الفلاح - الإصدار 1.0.0",
                    onClick = { showAboutDialog = true }
                )
                
                Spacer(modifier = Modifier.weight(1f))
                
                Button(
                    onClick = { showLogoutDialog = true },
                    modifier = Modifier.fillMaxWidth().height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Icon(Icons.AutoMirrored.Outlined.Logout, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("تسجيل الخروج", style = MaterialTheme.typography.titleMedium)
                }
            }
            
            if (showLogoutDialog) {
                AlertDialog(
                    onDismissRequest = { showLogoutDialog = false },
                    title = { Text("تسجيل الخروج") },
                    text = { Text("هل أنت متأكد أنك تريد تسجيل الخروج من التطبيق؟") },
                    confirmButton = {
                        Button(
                            onClick = {
                                showLogoutDialog = false
                                onLogout()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("خروج")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showLogoutDialog = false }) {
                            Text("إلغاء")
                        }
                    }
                )
            }

            if (showAboutDialog) {
                AlertDialog(
                    onDismissRequest = { showAboutDialog = false },
                    title = { Text("حول التطبيق") },
                    text = { Text("تطبيق الفلاح\nالإصدار 1.0.0\nتطبيق زراعي متكامل يهدف إلى مساعدة المزارعين من خلال توفير معلومات دقيقة حول المحاصيل، الآفات، والمنتجات الزراعية، بالإضافة إلى مساعد ذكي زراعي.\n\nتطوير: فريق الفلاح") },
                    confirmButton = {
                        Button(onClick = { showAboutDialog = false }) {
                            Text("موافق")
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun SettingsItem(
    icon: ImageVector,
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

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
