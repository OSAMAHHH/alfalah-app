package com.example.alfalah.ui.screens.calendar

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Grass
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.outlined.Agriculture
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.MyCrop
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CalendarScreen(
    onNavigateToCrop: (String) -> Unit,
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var isLoading by remember { mutableStateOf(true) }
    var myCrops by remember { mutableStateOf<List<Crop>>(emptyList()) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        isLoading = true
        try {
            val userCrops = userServicesRepository.getMyCrops()
            val loadedCrops = mutableListOf<Crop>()
            for (myCrop in userCrops) {
                val result = firestoreRepository.getCropById(myCrop.cropId)
                val crop = result.getOrNull()
                if (crop != null) {
                    loadedCrops.add(crop)
                }
            }
            myCrops = loadedCrops
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            isLoading = false
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("التقويم الزراعي", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        }
    ) { padding ->
        if (isLoading) {
            LoadingState(modifier = Modifier.padding(padding))
        } else if (myCrops.isEmpty()) {
            EmptyState(
                icon = Icons.Outlined.Agriculture,
                title = "لا توجد محاصيل",
                message = "قم بإضافة محاصيل إلى حقلك من دليل المحاصيل لتظهر مهامها هنا",
                modifier = Modifier.padding(padding)
            )
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    Text(
                        text = "المهام الزراعية لمحاصيلك",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                }
                items(myCrops) { crop ->
                    CropTasksCard(crop = crop, onClick = { onNavigateToCrop(crop.id) })
                }
            }
        }
    }
}

@Composable
fun CropTasksCard(crop: Crop, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        shape = RoundedCornerShape(20.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = crop.name,
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))

            if (crop.plantingSeason.isNotBlank()) {
                TaskItem(
                    icon = Icons.Filled.DateRange,
                    title = "موسم الزراعة",
                    desc = crop.plantingSeason,
                    iconTint = MaterialTheme.colorScheme.tertiary
                )
                Spacer(modifier = Modifier.height(12.dp))
            }

            if (crop.irrigation.isNotBlank()) {
                TaskItem(
                    icon = Icons.Filled.WaterDrop,
                    title = "مواعيد الري",
                    desc = crop.irrigation,
                    iconTint = Color(0xFF0288D1)
                )
                Spacer(modifier = Modifier.height(12.dp))
            }

            if (crop.fertilization.isNotBlank()) {
                TaskItem(
                    icon = Icons.Filled.Eco,
                    title = "جدول التسميد",
                    desc = crop.fertilization,
                    iconTint = Color(0xFF388E3C)
                )
            }
        }
    }
}

@Composable
fun TaskItem(icon: ImageVector, title: String, desc: String, iconTint: Color) {
    Row(verticalAlignment = Alignment.Top) {
        Box(
            modifier = Modifier
                .size(40.dp)
                .background(iconTint.copy(alpha = 0.15f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = icon, contentDescription = null, tint = iconTint, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = desc, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
