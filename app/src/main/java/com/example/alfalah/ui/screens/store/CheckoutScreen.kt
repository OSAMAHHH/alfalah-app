package com.example.alfalah.ui.screens.store

import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AccountBalanceWallet
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.res.painterResource
import androidx.compose.foundation.Image
import com.example.alfalah.R
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import coil.compose.SubcomposeAsyncImage
import com.example.alfalah.data.model.CartItem
import com.example.alfalah.data.model.Order
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.utils.CurrencyUtils
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CheckoutScreen(
    onBack: () -> Unit,
    onOrderSuccess: () -> Unit,
    userRepo: UserServicesRepository = remember { UserServicesRepository() },
    authRepo: AuthRepository = remember { AuthRepository() },
    firestoreRepo: FirestoreRepository = remember { FirestoreRepository() }
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    var items by remember { mutableStateOf<List<CartItem>>(emptyList()) }
    var totalAmount by remember { mutableStateOf(0.0) }
    var currency by remember { mutableStateOf("YER") }
    
    // User Info
    var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var governorate by remember { mutableStateOf("") }
    var address by remember { mutableStateOf("") }
    
    // Payment
    var paymentReference by remember { mutableStateOf("") }
    var paymentProofUri by remember { mutableStateOf<Uri?>(null) }
    
    var isLoading by remember { mutableStateOf(true) }
    var isSubmitting by remember { mutableStateOf(false) }
    
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri -> if (uri != null) paymentProofUri = uri }
    )

    LaunchedEffect(Unit) {
        scope.launch {
            
            val user = authRepo.currentUser.value
            if (user != null) {
                name = user.name
                phone = user.phone
                governorate = user.governorate
                address = user.address
            }

            
            val cartResult = userRepo.getCartItems()
            if (cartResult.isSuccess) {
                items = cartResult.getOrDefault(emptyList())
                totalAmount = items.sumOf { it.price * it.quantity }
                currency = items.firstOrNull()?.currency ?: "YER"
            }
            isLoading = false
        }
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("إتمام الطلب والدفع", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            },
            bottomBar = {
                if (!isLoading) {
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
                            Button(
                                onClick = {
                                    if (name.isBlank() || phone.isBlank() || governorate.isBlank() || address.isBlank()) {
                                        Toast.makeText(context, "الرجاء تعبئة جميع بيانات التوصيل", Toast.LENGTH_SHORT).show()
                                        return@Button
                                    }
                                    if (paymentReference.isBlank() && paymentProofUri == null) {
                                        Toast.makeText(context, "الرجاء إدخال رقم الحوالة أو إرفاق صورة السند", Toast.LENGTH_SHORT).show()
                                        return@Button
                                    }
                                    
                                    isSubmitting = true
                                    scope.launch {
                                        // Update user info
                                        authRepo.updateDeliveryInfo(phone, governorate, address)
                                        
                                        var proofUrl = ""
                                        if (paymentProofUri != null) {
                                            val uploadResult = userRepo.uploadPaymentReceipt(paymentProofUri!!)
                                            if (uploadResult.isSuccess) {
                                                proofUrl = uploadResult.getOrNull() ?: ""
                                            }
                                        }
                                        
                                        val order = Order(
                                            customerName = name,
                                            phone = phone,
                                            governorate = governorate,
                                            address = address,
                                            items = items,
                                            totalAmount = totalAmount,
                                            currency = currency,
                                            paymentMethod = "jeeb",
                                            paymentReference = paymentReference,
                                            paymentProofUrl = proofUrl,
                                            paymentStatus = "submitted"
                                        )
                                        
                                        val orderResult = userRepo.createOrder(order)
                                        if (orderResult.isSuccess) {
                                            userRepo.clearCart()
                                            Toast.makeText(context, "تم إرسال الطلب بنجاح. سيتم مراجعته قريباً.", Toast.LENGTH_LONG).show()
                                            onOrderSuccess()
                                        } else {
                                            Toast.makeText(context, "حدث خطأ أثناء إنشاء الطلب", Toast.LENGTH_SHORT).show()
                                            isSubmitting = false
                                        }
                                    }
                                },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp),
                                shape = RoundedCornerShape(12.dp),
                                enabled = !isSubmitting
                            ) {
                                if (isSubmitting) {
                                    CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                                } else {
                                    Text("تأكيد وإرسال الطلب", style = MaterialTheme.typography.titleMedium)
                                }
                            }
                        }
                    }
                }
            }
        ) { paddingValues ->
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .imePadding()
                        .padding(horizontal = 16.dp),
                    contentPadding = PaddingValues(vertical = 16.dp),
                    verticalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                    item {
                        // Order Summary
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)
                                .navigationBarsPadding()) {
                                Text("إجمالي المطلوب:", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    CurrencyUtils.formatPrice(totalAmount, currency),
                                    style = MaterialTheme.typography.displaySmall,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            }
                        }
                    }

                    item {
                        Text("بيانات التوصيل", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = name,
                            onValueChange = { name = it },
                            label = { Text("الاسم الكامل") },
                            leadingIcon = { Icon(Icons.Outlined.Person, contentDescription = null) },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = phone,
                            onValueChange = { phone = it },
                            label = { Text("رقم الهاتف") },
                            leadingIcon = { Icon(Icons.Outlined.Phone, contentDescription = null) },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = governorate,
                            onValueChange = { governorate = it },
                            label = { Text("المحافظة / المنطقة") },
                            leadingIcon = { Icon(Icons.Outlined.LocationOn, contentDescription = null) },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        OutlinedTextField(
                            value = address,
                            onValueChange = { address = it },
                            label = { Text("العنوان التفصيلي") },
                            leadingIcon = { Icon(Icons.Outlined.LocationOn, contentDescription = null) },
                            modifier = Modifier.fillMaxWidth(),
                            minLines = 2
                        )
                    }

                    item {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Image(
                                painter = painterResource(id = R.drawable.jeeb_logo),
                                contentDescription = "شعار جيب",
                                modifier = Modifier.size(32.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("الدفع يدوياً عبر تطبيق جيب", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)
                                .navigationBarsPadding()) {
                                Text("الخطوات:", fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("1. افتح تطبيق جيب.")
                                Text("2. قم بتحويل المبلغ الموضح أعلاه إلى الرقم: 777777777")
                                Text("3. أدخل رقم العملية (المرجع) في الحقل أدناه أو أرفق صورة السند.")
                                Spacer(modifier = Modifier.height(16.dp))
                                
                                OutlinedTextField(
                                    value = paymentReference,
                                    onValueChange = { paymentReference = it },
                                    label = { Text("رقم مرجع التحويل (اختياري إذا أرفقت صورة)") },
                                    leadingIcon = { Icon(Icons.Outlined.AccountBalanceWallet, contentDescription = null) },
                                    modifier = Modifier.fillMaxWidth()
                                )
                                Spacer(modifier = Modifier.height(16.dp))
                                
                                Text("إثبات الدفع (صورة السند):", style = MaterialTheme.typography.bodyMedium)
                                Spacer(modifier = Modifier.height(8.dp))
                                
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(120.dp)
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(MaterialTheme.colorScheme.surface)
                                        .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(8.dp))
                                        .clickable {
                                            imagePickerLauncher.launch(
                                                androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                                            )
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    if (paymentProofUri != null) {
                                        SubcomposeAsyncImage(
                                            model = paymentProofUri,
                                            contentDescription = "صورة السند",
                                            modifier = Modifier.fillMaxSize(),
                                            contentScale = ContentScale.Crop
                                        )
                                    } else {
                                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                            Icon(Icons.Outlined.Image, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                            Spacer(modifier = Modifier.height(4.dp))
                                            Text("اضغط لإرفاق صورة", color = MaterialTheme.colorScheme.onSurfaceVariant)
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
