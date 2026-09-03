package com.example.alfalah.ui.screens.store

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.outlined.RemoveShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import coil.compose.SubcomposeAsyncImage
import com.example.alfalah.data.model.CartItem
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import com.example.alfalah.utils.CurrencyUtils
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CartScreen(
    onBack: () -> Unit,
    onCheckout: () -> Unit,
    userRepo: UserServicesRepository = remember { UserServicesRepository() }
) {
    val scope = rememberCoroutineScope()
    var items by remember { mutableStateOf<List<CartItem>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var isUpdating by remember { mutableStateOf(false) }

    fun loadCart() {
        scope.launch {
            val result = userRepo.getCartItems()
            if (result.isSuccess) {
                items = result.getOrDefault(emptyList())
            }
            isLoading = false
        }
    }

    LaunchedEffect(Unit) {
        loadCart()
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("سلة المشتريات", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        if (items.isNotEmpty()) {
                            IconButton(onClick = {
                                scope.launch {
                                    isUpdating = true
                                    userRepo.clearCart()
                                    loadCart()
                                    isUpdating = false
                                }
                            }, enabled = !isUpdating) {
                                Icon(Icons.Filled.Delete, contentDescription = "تفريغ السلة")
                            }
                        }
                    }
                )
            },
            bottomBar = {
                if (items.isNotEmpty()) {
                    Surface(
                        color = MaterialTheme.colorScheme.surface,
                        tonalElevation = 8.dp,
                        shadowElevation = 8.dp
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp)
                                .navigationBarsPadding()
                        ) {
                            val total = items.sumOf { it.price * it.quantity }
                            val currency = items.firstOrNull()?.currency ?: "YER"
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("الإجمالي:", style = MaterialTheme.typography.titleMedium)
                                Text(
                                    CurrencyUtils.formatPrice(total, currency),
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            }
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(
                                onClick = onCheckout,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp),
                                shape = RoundedCornerShape(12.dp),
                                enabled = !isUpdating
                            ) {
                                Text("إتمام الطلب", style = MaterialTheme.typography.titleMedium)
                            }
                        }
                    }
                }
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.fillMaxSize().padding(paddingValues))
            } else if (items.isEmpty()) {
                EmptyState(
                    icon = Icons.Outlined.RemoveShoppingCart,
                    title = "سلة المشتريات فارغة",
                    message = "قم بإضافة بعض المنتجات من المتجر",
                    modifier = Modifier.fillMaxSize().padding(paddingValues)
                )
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .padding(horizontal = 16.dp),
                    contentPadding = PaddingValues(vertical = 16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(items) { item ->
                        CartItemCard(
                            item = item,
                            isUpdating = isUpdating,
                            onUpdateQuantity = { qty ->
                                scope.launch {
                                    isUpdating = true
                                    userRepo.updateCartQuantity(item.productId, qty)
                                    loadCart()
                                    isUpdating = false
                                }
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun CartItemCard(
    item: CartItem,
    isUpdating: Boolean,
    onUpdateQuantity: (Int) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.surface)
            ) {
                if (item.imageUrl.isNotEmpty()) {
                    SubcomposeAsyncImage(
                        model = item.imageUrl,
                        contentDescription = null,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop,
                        loading = { CircularProgressIndicator(modifier = Modifier.align(Alignment.Center).size(24.dp)) }
                    )
                }
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(item.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Spacer(modifier = Modifier.height(4.dp))
                Text(CurrencyUtils.formatPrice(item.price, item.currency), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    IconButton(
                        onClick = { onUpdateQuantity(item.quantity - 1) },
                        modifier = Modifier
                            .size(32.dp)
                            .background(MaterialTheme.colorScheme.surface, CircleShape),
                        enabled = !isUpdating
                    ) {
                        Icon(if (item.quantity > 1) Icons.Filled.Remove else Icons.Filled.Delete, contentDescription = "تقليل", modifier = Modifier.size(16.dp))
                    }
                    Text("${item.quantity}", style = MaterialTheme.typography.titleMedium)
                    IconButton(
                        onClick = { onUpdateQuantity(item.quantity + 1) },
                        modifier = Modifier
                            .size(32.dp)
                            .background(MaterialTheme.colorScheme.primaryContainer, CircleShape),
                        enabled = !isUpdating
                    ) {
                        Icon(Icons.Filled.Add, contentDescription = "زيادة", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.onPrimaryContainer)
                    }
                }
            }
        }
    }
}
