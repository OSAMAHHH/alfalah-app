package com.example.alfalah.ui.screens.store

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.FirestoreRepository
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductDetailsScreen(
    productId: String,
    onBack: () -> Unit,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var product by remember { mutableStateOf<Product?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    
    LaunchedEffect(productId) {
        val res = firestoreRepository.getProductById(productId)
        product = res.getOrNull()
        isLoading = false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(product?.name ?: "تفاصيل المنتج") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "رجوع")
                    }
                }
            )
        }
    ) { padding ->
        if (isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (product == null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                Text("المنتج غير موجود")
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (product!!.recommended) {
                        Badge(containerColor = MaterialTheme.colorScheme.primaryContainer, contentColor = MaterialTheme.colorScheme.primary) {
                            Text("⭐ موصى به", modifier = Modifier.padding(4.dp))
                        }
                    }
                    if (product!!.tested) {
                        Badge(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurfaceVariant) {
                            Text("✓ منتج مجرب", modifier = Modifier.padding(4.dp))
                        }
                    }
                }
                Text(product!!.name, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("السعر: ${product!!.price} ر.س", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                HorizontalDivider()
                
                if (product!!.category.isNotEmpty()) {
                    Text("التصنيف: ${product!!.category}", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)
                }
                
                Text("الوصف:", fontWeight = FontWeight.Bold)
                Text(product!!.description)
                
                if (product!!.nutrients.isNotEmpty()) {
                    Text("العناصر الغذائية:", fontWeight = FontWeight.Bold)
                    Text(product!!.nutrients.joinToString(", "))
                }
                
                if (product!!.suitableCrops.isNotEmpty()) {
                    Text("المحاصيل المناسبة:", fontWeight = FontWeight.Bold)
                    Text(product!!.suitableCrops.joinToString(", "))
                }
                
                if (product!!.suitableProblems.isNotEmpty()) {
                    Text("المشاكل التي يعالجها:", fontWeight = FontWeight.Bold)
                    Text(product!!.suitableProblems.joinToString(", "))
                }
                
                if (product!!.usage.isNotEmpty() || product!!.dosage.isNotEmpty()) {
                    HorizontalDivider()
                    Text("طريقة الاستخدام والجرعة:", fontWeight = FontWeight.Bold)
                    Text(product!!.usage)
                    Text(product!!.dosage)
                }
                
                if (product!!.warnings.isNotEmpty()) {
                    Text("تحذيرات:", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error)
                    Text(product!!.warnings, color = MaterialTheme.colorScheme.error)
                }
                
                Text("المخزون المتوفر: ${product!!.stock}", style = MaterialTheme.typography.bodySmall)

                Spacer(modifier = Modifier.weight(1f))
                Button(onClick = { /* TODO: Add to cart */ }, modifier = Modifier.fillMaxWidth().height(56.dp)) {
                    Text("إضافة إلى السلة")
                }
            }
        }
    }
}
