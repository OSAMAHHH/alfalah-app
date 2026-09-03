package com.example.alfalah.ui.screens.store

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.ImageNotSupported
import androidx.compose.material.icons.outlined.ShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import coil.compose.SubcomposeAsyncImage
import com.example.alfalah.data.model.CartItem
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import com.example.alfalah.utils.CurrencyUtils
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductDetailsScreen(
    productId: String,
    onBack: () -> Unit,
    onNavigateToCart: () -> Unit = {},
    modifier: Modifier = Modifier,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }
) {
    var product by remember { mutableStateOf<Product?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    var isFavorite by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    fun loadProduct() {
        scope.launch {
            isLoading = true
            errorMsg = null
            val result = firestoreRepository.getProductById(productId)
            if (result.isSuccess) {
                product = result.getOrNull()
                // Check if favorite
                val favs = userServicesRepository.getFavorites()
                isFavorite = favs.any { it.itemId == productId && it.itemType == "product" }
            } else {
                errorMsg = result.exceptionOrNull()?.message ?: "حدث خطأ غير معروف"
            }
            isLoading = false
        }
    }

    LaunchedEffect(productId) {
        loadProduct()
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("") },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent),
                    navigationIcon = {
                        IconButton(onClick = onBack, modifier = Modifier.background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f), androidx.compose.foundation.shape.CircleShape)) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        IconButton(onClick = {
                            scope.launch {
                                if (isFavorite) {
                                    val favs = userServicesRepository.getFavorites()
                                    val fav = favs.find { it.itemId == productId && it.itemType == "product" }
                                    if (fav != null) {
                                        val res = userServicesRepository.removeFavorite(fav.id)
                                        if (res.isSuccess) {
                                            isFavorite = false
                                            Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                } else {
                                    val res = userServicesRepository.addFavorite(productId, "product")
                                    if (res.isSuccess) {
                                        isFavorite = true
                                        Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                        }, modifier = Modifier.background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f), androidx.compose.foundation.shape.CircleShape)) {
                            Icon(
                                imageVector = if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                                contentDescription = "المفضلة",
                                tint = if (isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                            )
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        IconButton(onClick = onNavigateToCart, modifier = Modifier.background(MaterialTheme.colorScheme.surface.copy(alpha = 0.7f), androidx.compose.foundation.shape.CircleShape)) {
                            Icon(Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                        }
                    }
                )
            },
            bottomBar = {
                if (product != null) {
                    Surface(color = MaterialTheme.colorScheme.surface, shadowElevation = 16.dp, shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)) {
                        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp).navigationBarsPadding(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Column {
                                Text("السعر الإجمالي", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Text(CurrencyUtils.formatPrice(product?.price ?: 0.0, product?.currency ?: ""), style = MaterialTheme.typography.headlineSmall, color = MaterialTheme.colorScheme.primary)
                            }
                            Button(
                                onClick = {
                                    scope.launch {
                                        val item = CartItem(productId = product?.id ?: "", name = product?.name ?: "", price = product?.price ?: 0.0, currency = product?.currency?.ifEmpty { "YER" } ?: "YER", imageUrl = product?.imageUrl ?: "", quantity = 1)
                                        val result = userServicesRepository.addToCart(item)
                                        if (result.isSuccess) Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()
                                        else Toast.makeText(context, "حدث خطأ", Toast.LENGTH_SHORT).show()
                                    }
                                },
                                shape = RoundedCornerShape(16.dp),
                                contentPadding = PaddingValues(horizontal = 32.dp, vertical = 16.dp)
                            ) {
                                Icon(Icons.Filled.ShoppingCart, contentDescription = null)
                                Spacer(modifier = Modifier.width(12.dp))
                                Text("أضف للسلة", style = MaterialTheme.typography.titleMedium)
                            }
                        }
                    }
                }
            },
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ) { padding ->
            if (isLoading) {
                LoadingState(modifier = Modifier.fillMaxSize().padding(padding))
            } else if (product == null) {
                Column(modifier = Modifier.fillMaxSize().padding(padding), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                    EmptyState(
                        icon = Icons.Outlined.ShoppingCart,
                        title = "عذراً",
                        message = errorMsg ?: "المنتج غير موجود",
                        modifier = Modifier.weight(1f)
                    )
                    if (errorMsg != null) {
                        Button(onClick = { loadProduct() }, modifier = Modifier.padding(bottom = 32.dp)) {
                            Text("إعادة المحاولة")
                        }
                    }
                }
            } else {
                Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
                    Box(modifier = Modifier.fillMaxWidth().height(320.dp).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                        if (product?.imageUrl?.isNotEmpty() == true) {
                            SubcomposeAsyncImage(
                                model = product?.imageUrl,
                                contentDescription = null,
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Crop,
                                loading = {
                                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                                        CircularProgressIndicator(modifier = Modifier.size(24.dp))
                                    }
                                },
                                error = {
                                    Icon(Icons.Outlined.ImageNotSupported, contentDescription = null, modifier = Modifier.size(48.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                                }
                            )
                        } else {
                            Icon(Icons.Filled.Eco, contentDescription = null, modifier = Modifier.size(120.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f))
                        }
                    }
                    Column(
                        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp)).background(MaterialTheme.colorScheme.background).offset(y = (-32).dp).padding(32.dp)
                    ) {
                        Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(8.dp)) {
                            Text(product?.category ?: "".ifEmpty { "عام" }, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onPrimaryContainer, modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp))
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(product?.name ?: "", style = MaterialTheme.typography.headlineMedium, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(32.dp))
                        
                        Text("الوصف", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(product?.description ?: "", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.5f)
                        
                        if ((product?.usage?.isNotBlank() == true)) {
                            Spacer(modifier = Modifier.height(24.dp))
                            Text("طريقة الاستخدام", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(product?.usage ?: "", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.5f)
                        }
                        
                        if ((product?.dosage?.isNotBlank() == true)) {
                            Spacer(modifier = Modifier.height(24.dp))
                            Text("الجرعة", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(product?.dosage ?: "", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.5f)
                        }
                        
                        if ((product?.warnings?.isNotBlank() == true)) {
                            Spacer(modifier = Modifier.height(24.dp))
                            Surface(color = MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.5f), shape = RoundedCornerShape(16.dp)) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text("تنبيهات هامة", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onErrorContainer)
                                    Spacer(modifier = Modifier.height(8.dp))
                                    Text(product?.warnings ?: "", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onErrorContainer)
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(100.dp))
                    }
                }
            }
        }
    }
}
