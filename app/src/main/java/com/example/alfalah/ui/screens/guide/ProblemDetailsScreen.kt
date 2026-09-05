package com.example.alfalah.ui.screens.guide

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.SmartToy
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.AgriculturalProblem
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.LoadingState
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProblemDetailsScreen(
    problemId: String,
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    onNavigateToChatWithQuery: (String) -> Unit,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }
) {
    var problem by remember { mutableStateOf<AgriculturalProblem?>(null) }
    var relatedCrop by remember { mutableStateOf<Crop?>(null) }
    var recommendedProducts by remember { mutableStateOf<List<Product>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var isFavorite by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    LaunchedEffect(problemId) {
        val problemRes = firestoreRepository.getProblemById(problemId)
        if (problemRes.isSuccess) {
            problem = problemRes.getOrNull()
            if (problem != null) {
                isFavorite = userServicesRepository.isFavorite(problemId)
                
                if ((problem?.cropId?.isNotEmpty() == true)) {
                    firestoreRepository.getCropById(problem?.cropId ?: "").getOrNull()?.let {
                        relatedCrop = it
                    }
                }
                
                if ((problem?.recommendedProductIds?.isNotEmpty() == true)) {
                    firestoreRepository.getProductsByIds(problem?.recommendedProductIds ?: emptyList()).getOrNull()?.let {
                        recommendedProducts = it
                    }
                }
            }
        }
        isLoading = false
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text(problem?.name ?: "تفاصيل المشكلة", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        if (problem != null) {
                            IconButton(onClick = {
                                scope.launch {
                                    if (isFavorite) {
                                        if (userServicesRepository.removeFavorite(problemId).isSuccess) {
                                            isFavorite = false
                                            Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                        }
                                    } else {
                                        if (userServicesRepository.addFavorite(problemId, "problem").isSuccess) {
                                            isFavorite = true
                                            Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                }
                            }) {
                                Icon(
                                    if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                                    contentDescription = "المفضلة",
                                    tint = if (isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                                )
                            }
                        }
                    }
                )
            },
            floatingActionButton = {
                if (problem != null) {
                    ExtendedFloatingActionButton(
                        onClick = { onNavigateToChatWithQuery("كيف أعالج مشكلة ${problem?.name}${if (relatedCrop != null) " في محصول " + relatedCrop?.name ?: "" else ""}؟") },
                        icon = { Icon(Icons.Outlined.SmartToy, contentDescription = null) },
                        text = { Text("اسأل المساعد") },
                        containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                        contentColor = MaterialTheme.colorScheme.onTertiaryContainer
                    )
                }
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.padding(paddingValues))
            } else if (problem == null) {
                Box(modifier = Modifier.fillMaxSize().padding(paddingValues), contentAlignment = Alignment.Center) {
                    Text("المشكلة غير موجودة أو تم حذفها")
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    item {
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text("النوع: ${problem?.type ?: ""}", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onErrorContainer)
                                if (relatedCrop != null) {
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("المحصول المرتبط: ${relatedCrop?.name ?: ""}", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onErrorContainer, fontWeight = FontWeight.Bold)
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                
                                if ((problem?.symptoms?.isNotEmpty() == true)) DetailSection("🚨 الأعراض", problem?.symptoms?.joinToString("، ") ?: "")
                                if ((problem?.causes?.isNotEmpty() == true)) DetailSection("🔬 الأسباب", problem?.causes ?: "")
                                if ((problem?.treatment?.isNotEmpty() == true)) DetailSection("🩺 العلاج", problem?.treatment ?: "")
                                if ((problem?.prevention?.isNotEmpty() == true)) DetailSection("🛡️ الوقاية", problem?.prevention ?: "")
                            }
                        }
                    }

                    if (recommendedProducts.isNotEmpty()) {
                        item {
                            Text(
                                "🛒 المنتجات المقترحة",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.padding(vertical = 8.dp)
                            )
                        }
                        
                        items(recommendedProducts.size) { index ->
                            val product = recommendedProducts[index]
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                onClick = { onNavigateToProduct(product.id) },
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column {
                                        Text(product.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                        Text(com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary)
                                    }
                                }
                            }
                        }
                        
                        item {
                            Spacer(modifier = Modifier.height(64.dp))
                        }
                    }
                }
            }
        }
    }
}
