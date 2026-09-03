import re

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# I will rewrite the whole HomeScreen.kt to match requirements properly.

new_home = """package com.example.alfalah.ui.screens.home

import android.Manifest
import android.content.pm.PackageManager
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.automirrored.outlined.Logout
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.AdminPanelSettings
import androidx.compose.material.icons.outlined.BugReport
import androidx.compose.material.icons.outlined.Search
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.data.repository.WeatherInfo
import com.example.alfalah.data.repository.WeatherRepository
import com.google.android.gms.location.LocationServices
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    authRepository: AuthRepository,
    weatherRepository: WeatherRepository = remember { WeatherRepository() },
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },
    onNavigateToStore: () -> Unit,
    onNavigateToChat: () -> Unit,
    onNavigateToAdmin: () -> Unit,
    onNavigateToGuide: (String) -> Unit,
    onNavigateToProduct: (String) -> Unit = {},
    onNavigateToCrop: (String) -> Unit = {},
    onLogout: () -> Unit,
    modifier: Modifier = Modifier
) {
    val currentUser by authRepository.currentUser.collectAsState()
    val scope = rememberCoroutineScope()
    var weather by remember { mutableStateOf<WeatherInfo?>(null) }
    var weatherLoading by remember { mutableStateOf(true) }
    var locationError by remember { mutableStateOf<String?>(null) }

    var myCrops by remember { mutableStateOf<List<Crop>>(emptyList()) }
    var myCropsLoading by remember { mutableStateOf(true) }
    
    var featuredProducts by remember { mutableStateOf<List<Product>>(emptyList()) }
    var productsLoading by remember { mutableStateOf(true) }

    val context = LocalContext.current
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }

    fun fetchWeather() {
        weatherLoading = true
        locationError = null
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                            if (weather == null) locationError = "فشل في جلب بيانات الطقس"
                            weatherLoading = false
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                        weatherLoading = false
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
                weatherLoading = false
            }
        } else {
            locationError = "فعّل الموقع لعرض الطقس في منطقتك"
            weatherLoading = false
        }
    }

    val locationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        fetchWeather()
    }

    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            fetchWeather()
        } else {
            locationPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
        }
        
        // Fetch My Crops
        scope.launch {
            if (currentUser != null) {
                val cropIdsRes = userServicesRepository.getMyCrops()
                if (cropIdsRes.isSuccess) {
                    val ids = cropIdsRes.getOrNull()?.map { it.itemId } ?: emptyList()
                    if (ids.isNotEmpty()) {
                        // For simplicity, just get top 3
                        val list = mutableListOf<Crop>()
                        for (id in ids.take(3)) {
                            firestoreRepository.getCropById(id).getOrNull()?.let { list.add(it) }
                        }
                        myCrops = list
                    }
                }
            }
            myCropsLoading = false
        }
        
        // Fetch Products
        scope.launch {
            val res = firestoreRepository.getProductsPaginated(5, null)
            if (res.isSuccess) {
                featuredProducts = res.getOrNull()?.first ?: emptyList()
            }
            productsLoading = false
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
                        val name = currentUser?.name?.split(" ")?.firstOrNull() ?: "مزارعنا الكريم"
                        Text("مرحباً، $name 👋", style = MaterialTheme.typography.headlineMedium, color = MaterialTheme.colorScheme.onBackground)
                    }
                    if (currentUser != null) {
                        IconButton(
                            onClick = { authRepository.logout(); onLogout() },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surface, CircleShape).size(48.dp)
                        ) {
                            Icon(Icons.AutoMirrored.Outlined.Logout, contentDescription = "خروج", tint = MaterialTheme.colorScheme.primary)
                        }
                    } else {
                        IconButton(
                            onClick = onLogout,
                            modifier = Modifier.background(MaterialTheme.colorScheme.surface, CircleShape).size(48.dp)
                        ) {
                            Icon(Icons.Filled.Person, contentDescription = "تسجيل الدخول", tint = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }

            // Weather Card
            ElevatedCard(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp).offset(y = (-20).dp),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(20.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (weatherLoading) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            CircularProgressIndicator(modifier = Modifier.size(24.dp))
                            Spacer(modifier = Modifier.width(16.dp))
                            Text("جاري جلب الطقس...", style = MaterialTheme.typography.bodyMedium)
                        }
                    } else if (locationError != null || weather == null) {
                        Column {
                            Text(locationError ?: "تعذر جلب الطقس", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.error)
                            Spacer(modifier = Modifier.height(8.dp))
                            Button(onClick = {
                                if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                                    locationPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
                                } else {
                                    fetchWeather()
                                }
                            }, contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp)) {
                                Text("تحديث الطقس")
                            }
                        }
                    } else {
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
                                Text(weather?.description ?: "", style = MaterialTheme.typography.titleSmall, color = MaterialTheme.colorScheme.onSurface)
                                Text("${weather?.city ?: ""} - ${weather?.temperature ?: ""}°", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // AI Assistant Card
            Column(modifier = Modifier.padding(horizontal = 24.dp)) {
                FeatureCard(
                    title = "اسأل المساعد الزراعي",
                    subtitle = "احصل على مساعدة حول محاصيلك ومشاكلك الزراعية",
                    icon = Icons.Outlined.SmartToy,
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    onClick = onNavigateToChat
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Guide Shortcuts
            Text("استكشف الدليل الزراعي", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(horizontal = 24.dp), color = MaterialTheme.colorScheme.onBackground)
            Spacer(modifier = Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                SmallCategoryCard(title = "المحاصيل", icon = Icons.Filled.Eco, onClick = { onNavigateToGuide("crops") }, modifier = Modifier.weight(1f))
                SmallCategoryCard(title = "الآفات والأمراض", icon = Icons.Outlined.BugReport, onClick = { onNavigateToGuide("pests") }, modifier = Modifier.weight(1f))
                SmallCategoryCard(title = "البحث", icon = Icons.Outlined.Search, onClick = { onNavigateToGuide("search") }, modifier = Modifier.weight(1f))
            }

            Spacer(modifier = Modifier.height(32.dp))

            // My Crops
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("محاصيلي", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                if (myCrops.isNotEmpty()) {
                    TextButton(onClick = { /* Navigate to MyCrops which is in Profile actually, or we can just navigate to MY_CROPS route */ }) {
                        Text("عرض الكل")
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            if (myCropsLoading) {
                Box(modifier = Modifier.fillMaxWidth().height(100.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (myCrops.isEmpty()) {
                OutlinedCard(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                    colors = CardDefaults.outlinedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column(modifier = Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Filled.Eco, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(40.dp))
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("أضف محاصيلك للحصول على تجربة زراعية أكثر تخصيصاً", style = MaterialTheme.typography.bodyMedium, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { onNavigateToGuide("crops") }) {
                            Text("تصفح المحاصيل")
                        }
                    }
                }
            } else {
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 24.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(myCrops) { crop ->
                        ElevatedCard(
                            onClick = { onNavigateToCrop(crop.id) },
                            modifier = Modifier.width(140.dp).height(100.dp),
                            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                                Text(crop.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Products
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("المتجر الزراعي", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                if (featuredProducts.isNotEmpty()) {
                    TextButton(onClick = onNavigateToStore) {
                        Text("عرض المتجر")
                    }
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            if (productsLoading) {
                Box(modifier = Modifier.fillMaxWidth().height(120.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (featuredProducts.isEmpty()) {
                OutlinedCard(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                    colors = CardDefaults.outlinedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                        Text("لا توجد منتجات حالياً", style = MaterialTheme.typography.bodyMedium)
                    }
                }
            } else {
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 24.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(featuredProducts) { product ->
                        ElevatedCard(
                            onClick = { onNavigateToProduct(product.id) },
                            modifier = Modifier.width(160.dp),
                            colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(product.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, maxLines = 1)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("${product.price} ${product.currency}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                }
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
"""

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w", encoding="utf-8") as f:
    f.write(new_home)
