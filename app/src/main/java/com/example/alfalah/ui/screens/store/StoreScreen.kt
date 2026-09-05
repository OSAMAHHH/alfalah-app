package com.example.alfalah.ui.screens.store

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.AddShoppingCart
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.ImageNotSupported
import androidx.compose.material.icons.outlined.SearchOff
import androidx.compose.material.icons.outlined.ShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
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
fun StoreScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    onNavigateToCart: () -> Unit = {},
    modifier: Modifier = Modifier,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }
) {
    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var cartItemsCount by remember { mutableStateOf(0) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    fun loadData() {
        isLoading = true
        errorMsg = null
        scope.launch {
            try {
                val result = firestoreRepository.getProducts()
                if (result.isSuccess) {
                    products = result.getOrDefault(emptyList())
                    userServicesRepository.getCartItems().onSuccess { items ->
                        cartItemsCount = items.size
                    }
                } else {
                    errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                }
            } catch (e: Exception) {
                errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
            } finally {
                isLoading = false
            }
        }
    }

    LaunchedEffect(Unit) {
        loadData()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("المتجر الزراعي", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                    }
                },
                actions = {
                    IconButton(onClick = onNavigateToCart) {
                        BadgedBox(badge = { if (cartItemsCount > 0) Badge { Text(cartItemsCount.toString()) } }) {
                            Icon(Icons.Outlined.ShoppingCart, contentDescription = "السلة")
                        }
                    }
                }
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNavigateToCart,
                icon = { Icon(Icons.Outlined.ShoppingCart, contentDescription = "السلة") },
                text = { Text("السلة") },
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            )
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        if (isLoading) {
            LoadingState(modifier = Modifier.padding(padding))
        } else if (errorMsg != null) {
            Column(modifier = Modifier.fillMaxSize().padding(padding), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                EmptyState(
                    icon = Icons.Outlined.SearchOff,
                    title = "عذراً",
                    message = errorMsg ?: "",
                    modifier = Modifier.weight(1f)
                )
                Button(onClick = { loadData() }, modifier = Modifier.padding(bottom = 32.dp)) {
                    Text("إعادة المحاولة")
                }
            }
        } else if (products.isEmpty()) {
            EmptyState(
                icon = Icons.Outlined.SearchOff,
                title = "المتجر فارغ",
                message = "لا تتوفر منتجات في الوقت الحالي، يرجى العودة لاحقاً.",
                modifier = Modifier.padding(padding)
            )
        } else {
            LazyVerticalGrid(
                columns = GridCells.Adaptive(minSize = 160.dp),
                modifier = modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(products) { product ->
                    ProductCard(
                        product = product,
                        onClick = { onNavigateToProduct(product.id) },
                        onAddToCart = { p ->
                            scope.launch {
                                val item = CartItem(productId = p.id, name = p.name, price = p.price, currency = p.currency.ifEmpty { "YER" }, imageUrl = p.imageUrl, quantity = 1)
                                val result = userServicesRepository.addToCart(item)
                                if (result.isSuccess) {
                                    cartItemsCount += 1
                                    Toast.makeText(context, "تمت الإضافة للسلة", Toast.LENGTH_SHORT).show()
                                }
                                else Toast.makeText(context, result.exceptionOrNull()?.message ?: "حدث خطأ غير معروف", Toast.LENGTH_LONG).show()
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun ProductCard(product: Product, onClick: () -> Unit, onAddToCart: (Product) -> Unit) {
    ElevatedCard(
        onClick = onClick,
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column {
            Box(
                modifier = Modifier.fillMaxWidth().aspectRatio(1f).background(MaterialTheme.colorScheme.surfaceVariant),
                contentAlignment = Alignment.Center
            ) {
                if (product.imageUrl.isNotEmpty()) {
                    SubcomposeAsyncImage(
                        model = product.imageUrl,
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
                    Icon(Icons.Outlined.Eco, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                }
                Box(
                    modifier = Modifier.align(Alignment.TopStart).padding(12.dp).background(MaterialTheme.colorScheme.primaryContainer, RoundedCornerShape(8.dp)).padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(product.category.ifEmpty { "عام" }, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onPrimaryContainer)
                }
            }
            Column(modifier = Modifier.padding(16.dp)) {
                Text(product.name, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurface, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Spacer(modifier = Modifier.height(4.dp))
                Text(product.description, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis, modifier = Modifier.height(32.dp))
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text(CurrencyUtils.formatPrice(product.price, product.currency), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                    IconButton(
                        onClick = { onAddToCart(product) },
                        modifier = Modifier.size(36.dp).background(MaterialTheme.colorScheme.primary, CircleShape)
                    ) {
                        Icon(Icons.Filled.AddShoppingCart, contentDescription = "أضف", modifier = Modifier.size(18.dp), tint = MaterialTheme.colorScheme.onPrimary)
                    }
                }
            }
        }
    }
}
