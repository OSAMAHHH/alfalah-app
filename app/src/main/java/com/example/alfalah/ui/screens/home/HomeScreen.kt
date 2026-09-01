package com.example.alfalah.ui.screens.home

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.automirrored.outlined.Logout
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material.icons.outlined.AdminPanelSettings
import androidx.compose.material.icons.outlined.BugReport
import androidx.compose.material.icons.outlined.SmartToy
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.data.repository.WeatherRepository
import com.example.alfalah.data.repository.WeatherInfo
import androidx.compose.material.icons.filled.Cloud
import androidx.compose.material.icons.filled.CloudQueue
import androidx.compose.material.icons.filled.Thunderstorm
import androidx.compose.material.icons.filled.NightsStay
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationServices

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    authRepository: AuthRepository,
    weatherRepository: WeatherRepository = androidx.compose.runtime.remember { WeatherRepository() },
    onNavigateToStore: () -> Unit,
    onNavigateToChat: () -> Unit,
    onNavigateToAdmin: () -> Unit,
    onNavigateToGuide: (String) -> Unit,
    onLogout: () -> Unit,
    modifier: Modifier = Modifier
) {
    val currentUser by authRepository.currentUser.collectAsState()
    val scope = rememberCoroutineScope()
    var weather by remember { mutableStateOf<WeatherInfo?>(null) }
    
    
    val context = LocalContext.current
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }
    var locationError by remember { mutableStateOf<String?>(null) }
    
    val locationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
            }
        } else {
            locationError = "تم رفض إذن الموقع. نعرض لك طقس غير دقيق."
            scope.launch {
                weather = weatherRepository.getCurrentWeather(24.7136, 46.6753).getOrNull()
            }
        }
    }

    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
            }
        } else {
            locationPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }


    Scaffold(containerColor = MaterialTheme.colorScheme.background) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(padding)
        ) {
            // Hero Header
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        brush = Brush.verticalGradient(
                            colors = listOf(MaterialTheme.colorScheme.primaryContainer, MaterialTheme.colorScheme.background)
                        )
                    )
                    .padding(horizontal = 24.dp, vertical = 32.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("مرحباً بك،", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                        Text(currentUser?.name ?: "مزارعنا الكريم (زائر)", style = MaterialTheme.typography.headlineMedium, color = MaterialTheme.colorScheme.onBackground)
                    }
                    if (currentUser != null) {
                        IconButton(
                            onClick = { authRepository.logout(); onLogout() },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surface, CircleShape).size(48.dp)
                        ) {
                            Icon(Icons.AutoMirrored.Outlined.Logout, contentDescription = "خروج", tint = MaterialTheme.colorScheme.primary)
                        }
                    } else {
                        Button(onClick = onLogout, shape = RoundedCornerShape(12.dp)) {
                            Text("تسجيل الدخول")
                        }
                    }
                }
            }

            // Weather Widget
            
            if (locationError != null && weather == null) {
                Text(
                    text = locationError!!,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(horizontal = 24.dp)
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            ElevatedCard(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(20.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        val icon = when (weather?.code) {
                            0 -> if (weather?.isDay == true) Icons.Filled.WbSunny else Icons.Filled.NightsStay
                            in 1..3 -> Icons.Filled.CloudQueue
                            in 45..48 -> Icons.Filled.Cloud
                            in 51..65, in 80..82 -> Icons.Filled.WaterDrop
                            in 71..75 -> Icons.Filled.Cloud
                            in 95..99 -> Icons.Filled.Thunderstorm
                            else -> Icons.Filled.WbSunny
                        }
                        val iconTint = if (weather?.isDay != false && (weather?.code == 0 || weather?.code == null)) Color(0xFFF9A825) else MaterialTheme.colorScheme.primary
                        Icon(icon, contentDescription = null, tint = iconTint, modifier = Modifier.size(40.dp))
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text(weather?.description ?: "جاري جلب الطقس...", style = MaterialTheme.typography.titleSmall, color = MaterialTheme.colorScheme.onSurface)
                            Text(if (weather != null) "${weather!!.city} - ${weather!!.temperature}°" else "الرجاء الانتظار", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))
            Text("الخدمات الأساسية", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(horizontal = 24.dp), color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            
            Column(modifier = Modifier.padding(horizontal = 24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                FeatureCard(
                    title = "اسأل الفلاح",
                    subtitle = "مساعدك الذكي لتشخيص الأمراض واقتراح الحلول الفورية",
                    icon = Icons.Outlined.SmartToy,
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    onClick = onNavigateToChat
                )
                FeatureCard(
                    title = "المتجر الزراعي",
                    subtitle = "تسوق أفضل الأسمدة والمبيدات الموثوقة لمحصولك",
                    icon = Icons.Outlined.Storefront,
                    containerColor = MaterialTheme.colorScheme.secondaryContainer,
                    contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
                    onClick = onNavigateToStore
                )
            }

            Spacer(modifier = Modifier.height(32.dp))
            Text("دليل المزارع", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(horizontal = 24.dp), color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                SmallCategoryCard(title = "المحاصيل", icon = Icons.Filled.Eco, onClick = { onNavigateToGuide("crops") }, modifier = Modifier.weight(1f))
                SmallCategoryCard(title = "الآفات", icon = Icons.Outlined.BugReport, onClick = { onNavigateToGuide("pests") }, modifier = Modifier.weight(1f))
                SmallCategoryCard(title = "الري", icon = Icons.Filled.WaterDrop, onClick = { onNavigateToGuide("irrigation") }, modifier = Modifier.weight(1f))
            }

            if (currentUser?.role == "admin") {
                Spacer(modifier = Modifier.height(32.dp))
                OutlinedCard(
                    onClick = onNavigateToAdmin,
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp).height(80.dp),
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.outlinedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
                ) {
                    Row(modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.AdminPanelSettings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(modifier = Modifier.width(16.dp))
                        Text("لوحة تحكم المشرف (Admin)", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}

@Composable
fun FeatureCard(title: String, subtitle: String, icon: ImageVector, containerColor: Color, contentColor: Color, onClick: () -> Unit, modifier: Modifier = Modifier) {
    ElevatedCard(
        onClick = onClick,
        modifier = modifier.fillMaxWidth().height(140.dp),
        shape = RoundedCornerShape(28.dp),
        colors = CardDefaults.elevatedCardColors(containerColor = containerColor),
        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 0.dp)
    ) {
        Box(modifier = Modifier.fillMaxSize()) {
            Icon(imageVector = icon, contentDescription = null, modifier = Modifier.size(140.dp).align(Alignment.BottomEnd).offset(x = 32.dp, y = 32.dp), tint = contentColor.copy(alpha = 0.1f))
            Row(modifier = Modifier.fillMaxSize().padding(24.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(56.dp).background(contentColor.copy(alpha = 0.2f), CircleShape), contentAlignment = Alignment.Center) {
                    Icon(imageVector = icon, contentDescription = null, modifier = Modifier.size(32.dp), tint = contentColor)
                }
                Spacer(modifier = Modifier.width(20.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(text = title, style = MaterialTheme.typography.titleLarge, color = contentColor)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(text = subtitle, style = MaterialTheme.typography.bodySmall, color = contentColor.copy(alpha = 0.8f))
                }
                Icon(Icons.AutoMirrored.Outlined.ArrowForward, contentDescription = null, tint = contentColor.copy(alpha = 0.8f))
            }
        }
    }
}

@Composable
fun SmallCategoryCard(title: String, icon: ImageVector, onClick: () -> Unit, modifier: Modifier = Modifier) {
    OutlinedCard(
        modifier = modifier.aspectRatio(1f),
        onClick = onClick,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.outlinedCardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.3f))
    ) {
        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(imageVector = icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(36.dp))
            Spacer(modifier = Modifier.height(12.dp))
            Text(text = title, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurface)
        }
    }
}
