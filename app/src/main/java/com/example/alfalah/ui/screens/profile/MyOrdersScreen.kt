package com.example.alfalah.ui.screens.profile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.Order
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import com.example.alfalah.utils.CurrencyUtils
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyOrdersScreen(
    onBack: () -> Unit,
    userRepo: UserServicesRepository = remember { UserServicesRepository() }
) {
    var orders by remember { mutableStateOf<List<Order>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        scope.launch {
            val res = userRepo.getMyOrders()
            if (res.isSuccess) {
                orders = res.getOrDefault(emptyList())
            }
            isLoading = false
        }
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("طلباتي", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.fillMaxSize().padding(paddingValues))
            } else if (orders.isEmpty()) {
                EmptyState(
                    icon = Icons.AutoMirrored.Outlined.ArrowBack,
                    title = "لا توجد طلبات",
                    message = "لم تقم بأي طلبات بعد",
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
                    items(orders) { order ->
                        MyOrderCard(order)
                    }
                }
            }
        }
    }
}

@Composable
fun MyOrderCard(order: Order) {
    val df = remember { SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault()) }
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("طلب #${order.id.take(6).uppercase()}", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                Text(df.format(Date(order.createdAt)), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(CurrencyUtils.formatPrice(order.totalAmount, order.currency), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                
                val (text, color, bgColor) = when (order.orderStatus) {
                    "pending" -> Triple("قيد الانتظار", MaterialTheme.colorScheme.onSecondaryContainer, MaterialTheme.colorScheme.secondaryContainer)
                    "processing" -> Triple("قيد التجهيز", MaterialTheme.colorScheme.onTertiaryContainer, MaterialTheme.colorScheme.tertiaryContainer)
                    "completed" -> Triple("مكتمل", MaterialTheme.colorScheme.onPrimaryContainer, MaterialTheme.colorScheme.primaryContainer)
                    "rejected" -> Triple("مرفوض", MaterialTheme.colorScheme.onErrorContainer, MaterialTheme.colorScheme.errorContainer)
                    else -> Triple(order.orderStatus, MaterialTheme.colorScheme.onSurface, MaterialTheme.colorScheme.surface)
                }
                Surface(color = bgColor, shape = RoundedCornerShape(16.dp)) {
                    Text(text, color = color, style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                }
            }
        }
    }
}
