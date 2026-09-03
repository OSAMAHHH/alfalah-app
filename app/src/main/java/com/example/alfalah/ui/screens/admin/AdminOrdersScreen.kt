package com.example.alfalah.ui.screens.admin

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import coil.compose.SubcomposeAsyncImage
import com.example.alfalah.data.model.Order
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.utils.CurrencyUtils
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun AdminOrdersScreen(
    userRepo: UserServicesRepository = remember { UserServicesRepository() }
) {
    var orders by remember { mutableStateOf<List<Order>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var selectedOrder by remember { mutableStateOf<Order?>(null) }
    val scope = rememberCoroutineScope()

    fun loadOrders() {
        scope.launch {
            isLoading = true
            val res = userRepo.getAllOrders()
            if (res.isSuccess) {
                orders = res.getOrDefault(emptyList())
            }
            isLoading = false
        }
    }

    LaunchedEffect(Unit) { loadOrders() }

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else if (orders.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("لا توجد طلبات حالياً", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(orders) { order ->
                OrderCard(order) { selectedOrder = order }
            }
        }
    }

    if (selectedOrder != null) {
        OrderDetailsDialog(
            order = selectedOrder!!,
            onDismiss = { selectedOrder = null },
            onUpdateStatus = { paymentStatus, orderStatus ->
                scope.launch {
                    userRepo.updateOrderStatus(selectedOrder!!.id, paymentStatus, orderStatus)
                    loadOrders()
                    selectedOrder = null
                }
            }
        )
    }
}

@Composable
fun OrderCard(order: Order, onClick: () -> Unit) {
    val df = remember { SimpleDateFormat("yyyy/MM/dd HH:mm", Locale.getDefault()) }
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(order.customerName, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                Text(df.format(Date(order.createdAt)), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(CurrencyUtils.formatPrice(order.totalAmount, order.currency), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                StatusChip(status = order.orderStatus)
            }
        }
    }
}

@Composable
fun StatusChip(status: String) {
    val (text, color, bgColor) = when (status) {
        "pending" -> Triple("قيد الانتظار", MaterialTheme.colorScheme.onSecondaryContainer, MaterialTheme.colorScheme.secondaryContainer)
        "processing" -> Triple("قيد التجهيز", MaterialTheme.colorScheme.onTertiaryContainer, MaterialTheme.colorScheme.tertiaryContainer)
        "completed" -> Triple("مكتمل", MaterialTheme.colorScheme.onPrimaryContainer, MaterialTheme.colorScheme.primaryContainer)
        "rejected" -> Triple("مرفوض", MaterialTheme.colorScheme.onErrorContainer, MaterialTheme.colorScheme.errorContainer)
        else -> Triple(status, MaterialTheme.colorScheme.onSurface, MaterialTheme.colorScheme.surface)
    }
    Surface(color = bgColor, shape = RoundedCornerShape(16.dp)) {
        Text(text, color = color, style = MaterialTheme.typography.labelSmall, modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
    }
}

@Composable
fun OrderDetailsDialog(
    order: Order,
    onDismiss: () -> Unit,
    onUpdateStatus: (paymentStatus: String, orderStatus: String) -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("تفاصيل الطلب") },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                Text("العميل: ${order.customerName}", fontWeight = FontWeight.Bold)
                Text("رقم الهاتف: ${order.phone}")
                Text("العنوان: ${order.governorate} - ${order.address}")
                Spacer(modifier = Modifier.height(16.dp))
                
                Text("المنتجات:", fontWeight = FontWeight.Bold)
                order.items.forEach { item ->
                    Text("- ${item.name} (x${item.quantity})")
                }
                Spacer(modifier = Modifier.height(16.dp))
                
                Text("الإجمالي: ${CurrencyUtils.formatPrice(order.totalAmount, order.currency)}", color = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(16.dp))
                
                Text("معلومات الدفع:", fontWeight = FontWeight.Bold)
                Text("المرجع: ${order.paymentReference.ifEmpty { "غير متوفر" }}")
                if (order.paymentProofUrl.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("صورة السند:", style = MaterialTheme.typography.labelSmall)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(150.dp)
                            .clip(RoundedCornerShape(8.dp))
                    ) {
                        SubcomposeAsyncImage(
                            model = order.paymentProofUrl,
                            contentDescription = "السند",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                    }
                }
            }
        },
        confirmButton = {
            if (order.orderStatus != "completed" && order.orderStatus != "rejected") {
                Button(onClick = { onUpdateStatus("approved", "completed") }) {
                    Text("قبول الطلب")
                }
            }
        },
        dismissButton = {
            if (order.orderStatus != "completed" && order.orderStatus != "rejected") {
                TextButton(onClick = { onUpdateStatus("rejected", "rejected") }, colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)) {
                    Text("رفض")
                }
            }
        }
    )
}
