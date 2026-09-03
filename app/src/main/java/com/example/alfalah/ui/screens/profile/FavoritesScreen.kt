package com.example.alfalah.ui.screens.profile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.*
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import com.example.alfalah.ui.screens.guide.CropCard
import com.example.alfalah.ui.screens.guide.ProblemCard
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FavoritesScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    onNavigateToCrop: (String) -> Unit = {},
    onNavigateToProblem: (String) -> Unit = {},
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var favorites by remember { mutableStateOf<List<Favorite>>(emptyList()) }
    var loadedItems by remember { mutableStateOf<Map<String, Any>>(emptyMap()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        val favs = userServicesRepository.getFavorites()
        favorites = favs
        
        val itemsMap = mutableMapOf<String, Any>()
        for (fav in favs) {
            when (fav.itemType) {
                "crop" -> {
                    firestoreRepository.getCropById(fav.itemId).getOrNull()?.let { itemsMap[fav.itemId] = it }
                }
                "problem" -> {
                    firestoreRepository.getProblemById(fav.itemId).getOrNull()?.let { itemsMap[fav.itemId] = it }
                }
                "product" -> {
                    firestoreRepository.getProductById(fav.itemId).getOrNull()?.let { itemsMap[fav.itemId] = it }
                }
            }
        }
        loadedItems = itemsMap
        isLoading = false
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("المفضلة", fontWeight = FontWeight.Bold) },
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
            } else if (favorites.isEmpty()) {
                EmptyState(
                    icon = Icons.Filled.Favorite,
                    title = "لا توجد عناصر",
                    message = "لم تضف أي عناصر إلى المفضلة بعد",
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
                    items(favorites.size) { index ->
                        val fav = favorites[index]
                        val item = loadedItems[fav.itemId]
                        
                        if (item != null) {
                            when (item) {
                                is Crop -> CropCard(crop = item, userServicesRepository = userServicesRepository, onClick = { onNavigateToCrop(item.id) })
                                is AgriculturalProblem -> ProblemCard(problem = item, userServicesRepository = userServicesRepository, onClick = { onNavigateToProblem(item.id) })
                                is Product -> {
                                    Card(
                                        modifier = Modifier.fillMaxWidth(),
                                        onClick = { onNavigateToProduct(fav.itemId) }
                                    ) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth().padding(16.dp),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(item.name, style = MaterialTheme.typography.titleLarge)
                                            Text("منتج", style = MaterialTheme.typography.bodySmall)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
