package com.example.alfalah.ui.screens.profile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.MyCrop
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import com.example.alfalah.ui.screens.guide.CropCard
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyCropsScreen(
    onBack: () -> Unit,
    onNavigateToCrop: (String) -> Unit = {},
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var myCrops by remember { mutableStateOf<List<MyCrop>>(emptyList()) }
    var loadedCrops by remember { mutableStateOf<List<Crop>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        val cropsData = userServicesRepository.getMyCrops()
        myCrops = cropsData
        
        // Fetch crop details
        val fullCrops = mutableListOf<Crop>()
        for (myCrop in cropsData) {
            val cres = firestoreRepository.getCropById(myCrop.cropId)
            cres.getOrNull()?.let { fullCrops.add(it) }
        }
        loadedCrops = fullCrops
        isLoading = false
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("محاصيلي", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.padding(paddingValues))
            } else if (loadedCrops.isEmpty()) {
                EmptyState(
                    icon = Icons.Filled.Eco,
                    title = "لا توجد محاصيل",
                    message = "أضف المحاصيل التي تزرعها لمساعدتك بشكل أفضل",
                    modifier = Modifier.padding(paddingValues)
                )
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(loadedCrops.size) { index ->
                        CropCard(crop = loadedCrops[index], userServicesRepository = userServicesRepository, onClick = { onNavigateToCrop(loadedCrops[index].id) })
                    }
                }
            }
        }
    }
}
