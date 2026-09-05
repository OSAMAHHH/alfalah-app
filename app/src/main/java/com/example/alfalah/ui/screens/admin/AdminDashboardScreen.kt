package com.example.alfalah.ui.screens.admin

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import com.example.alfalah.data.repository.FirestoreRepository
import kotlinx.coroutines.launch
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.PickVisualMediaRequest
import android.content.Intent
import android.net.Uri
import com.example.alfalah.data.model.AgriculturalProblem
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.Product

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdminDashboardScreen(
    onBack: () -> Unit,
    onNavigateToImport: () -> Unit = {},
    modifier: Modifier = Modifier,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("المنتجات", "المحاصيل", "المشاكل", "الطلبات")
    
    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var crops by remember { mutableStateOf<List<Crop>>(emptyList()) }
    var problems by remember { mutableStateOf<List<AgriculturalProblem>>(emptyList()) }
    
    var isLoading by remember { mutableStateOf(true) }
    val scope = rememberCoroutineScope()

    var showProductDialog by remember { mutableStateOf<Product?>(null) }
    var showCropDialog by remember { mutableStateOf<Crop?>(null) }
    var showProblemDialog by remember { mutableStateOf<AgriculturalProblem?>(null) }
    var isAdding by remember { mutableStateOf(false) }
    var cropToDelete by remember { mutableStateOf<Crop?>(null) }
    var problemToDelete by remember { mutableStateOf<AgriculturalProblem?>(null) }

    fun loadData() {
        scope.launch {
            isLoading = true
            val productsResult = firestoreRepository.getProducts()
            val cropsResult = firestoreRepository.getCrops()
            val problemsResult = firestoreRepository.getProblems()
            
            products = productsResult.getOrDefault(emptyList())
            crops = cropsResult.getOrDefault(emptyList())
            problems = problemsResult.getOrDefault(emptyList())
            isLoading = false
        }
    }

    LaunchedEffect(Unit) { loadData() }

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = { Text("لوحة تحكم المشرف") },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        IconButton(onClick = onNavigateToImport) {
                            Icon(Icons.Outlined.Add, contentDescription = "استيراد")
                        }
                    }
                )
                TabRow(selectedTabIndex = selectedTab) {
                    tabs.forEachIndexed { index, title ->
                        Tab(
                            selected = selectedTab == index,
                            onClick = { selectedTab = index },
                            text = { Text(title) }
                        )
                    }
                }
            }
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = { 
                    isAdding = true
                    when (selectedTab) {
                        0 -> showProductDialog = Product()
                        1 -> showCropDialog = Crop()
                        2 -> showProblemDialog = AgriculturalProblem()
                    }
                },
                icon = { Icon(Icons.Outlined.Add, contentDescription = "إضافة") },
                text = { Text("إضافة جديد") },
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                shape = RoundedCornerShape(16.dp)
            )
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            if (isLoading) {
                com.example.alfalah.ui.components.LoadingState()
            } else {
                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false }, { c -> cropToDelete = c })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false }, { pr -> problemToDelete = pr })
                    3 -> AdminOrdersScreen()
                }
            }
        }

        if (showProductDialog != null) {
            ProductDialog(
                product = showProductDialog ?: Product(),
                isAdding = isAdding,
                onDismiss = { showProductDialog = null },
                onSave = { p ->
                    scope.launch {
                        val r = if (isAdding) firestoreRepository.addProduct(p) else firestoreRepository.updateProduct(p)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        showProductDialog = null
                        loadData()
                    }
                }
            )
        }
        
        if (showCropDialog != null) {
            CropDialog(
                crop = showCropDialog ?: Crop(),
                isAdding = isAdding,
                onDismiss = { showCropDialog = null },
                onSave = { c ->
                    scope.launch {
                        val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المحصول بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showCropDialog = null
                        loadData()
                    }
                }
            )
        }

        if (showProblemDialog != null) {
            ProblemDialog(
                problem = showProblemDialog ?: AgriculturalProblem(),
                crops = crops,
                products = products,
                isAdding = isAdding,
                onDismiss = { showProblemDialog = null },
                onSave = { pr ->
                    scope.launch {
                        val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المشكلة بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showProblemDialog = null
                        loadData()
                    }
                }
            )
        }

        if (cropToDelete != null) {
            AlertDialog(
                onDismissRequest = { cropToDelete = null },
                title = { Text("تأكيد الحذف") },
                text = { Text("هل أنت متأكد أنك تريد حذف المحصول '${cropToDelete ?: Crop().name}'؟") },
                confirmButton = {
                    Button(
                        onClick = { 
                            scope.launch {
                                isLoading = true
                                val r = firestoreRepository.deleteCrop(cropToDelete?.id ?: "")
                                if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                                else android.widget.Toast.makeText(context, "تم الحذف بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                                cropToDelete = null
                                loadData()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                    ) { Text("حذف") }
                },
                dismissButton = { TextButton(onClick = { cropToDelete = null }) { Text("إلغاء") } }
            )
        }

        if (problemToDelete != null) {
            AlertDialog(
                onDismissRequest = { problemToDelete = null },
                title = { Text("تأكيد الحذف") },
                text = { Text("هل أنت متأكد أنك تريد حذف المشكلة '${problemToDelete ?: AgriculturalProblem().name}'؟") },
                confirmButton = {
                    Button(
                        onClick = { 
                            scope.launch {
                                isLoading = true
                                val r = firestoreRepository.deleteProblem(problemToDelete?.id ?: "")
                                if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                                else android.widget.Toast.makeText(context, "تم الحذف بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                                problemToDelete = null
                                loadData()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                    ) { Text("حذف") }
                },
                dismissButton = { TextButton(onClick = { problemToDelete = null }) { Text("إلغاء") } }
            )
        }
    }
}

@Composable
fun ProductsList(products: List<Product>, onEdit: (Product) -> Unit, onDelete: (Product) -> Unit) {
    if (products.isEmpty()) {
        EmptyStateMessage("لا توجد منتجات")
        return
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(products) { product ->
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(product.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            "السعر: " + com.example.alfalah.utils.CurrencyUtils.formatPrice(product.price, product.currency), 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        StatusBadge(isActive = product.isActive)
                    }
                    Row {
                        IconButton(onClick = { onEdit(product) }) {
                            Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = { onDelete(product) }) {
                            Icon(Icons.Outlined.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CropsList(crops: List<Crop>, onEdit: (Crop) -> Unit, onDelete: (Crop) -> Unit) {
    if (crops.isEmpty()) {
        EmptyStateMessage("لا توجد محاصيل")
        return
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(crops) { crop ->
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(crop.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        StatusBadge(isActive = crop.isActive)
                    }
                    Row {
                        IconButton(onClick = { onEdit(crop) }) {
                            Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = { onDelete(crop) }) {
                            Icon(Icons.Outlined.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit, onDelete: (AgriculturalProblem) -> Unit) {
    if (problems.isEmpty()) {
        EmptyStateMessage("لا توجد مشاكل زراعية مسجلة")
        return
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(problems) { problem ->
            val cropName = crops.find { it.id == problem.cropId }?.name ?: "غير معروف"
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surface),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(problem.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            "المحصول: $cropName", 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        StatusBadge(isActive = problem.isActive)
                    }
                    Row {
                        IconButton(onClick = { onEdit(problem) }) {
                            Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = { onDelete(problem) }) {
                            Icon(Icons.Outlined.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun EmptyStateMessage(message: String) {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun StatusBadge(isActive: Boolean) {
    Surface(
        color = if (isActive) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(8.dp)
    ) {
        Text(
            text = if (isActive) "نشط" else "غير نشط",
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall,
            color = if (isActive) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductDialog(product: Product, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Product) -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val firestoreRepo = remember { FirestoreRepository() }
    
    var name by remember { mutableStateOf(product.name) }
    var priceStr by remember { mutableStateOf(if (product.price == 0.0) "" else product.price.toString()) }
    var description by remember { mutableStateOf(product.description) }
    var usage by remember { mutableStateOf(product.usage) }
    var warnings by remember { mutableStateOf(product.warnings) }
    var category by remember { mutableStateOf(product.category) }
    var currency by remember { mutableStateOf(product.currency.ifEmpty { "SAR" }) }
    var imageUrl by remember { mutableStateOf(product.imageUrl) }
    var isUploading by remember { mutableStateOf(false) }
    
    var expandedCurrency by remember { mutableStateOf(false) }
    
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri: android.net.Uri? ->
            if (uri != null) {
                isUploading = true
                scope.launch {
                    val result = firestoreRepo.uploadImage(uri)
                    isUploading = false
                    if (result.isSuccess) {
                        imageUrl = result.getOrNull() ?: ""
                    }
                }
            }
        }
    )
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة منتج جديد" else "تعديل منتج", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.verticalScroll(rememberScrollState())) {
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("اسم المنتج") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = description, onValueChange = { description = it }, label = { Text("الوصف") }, modifier = Modifier.fillMaxWidth())
                
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = priceStr, onValueChange = { priceStr = it }, label = { Text("السعر") }, modifier = Modifier.weight(1f))
                    ExposedDropdownMenuBox(expanded = expandedCurrency, onExpandedChange = { expandedCurrency = it }, modifier = Modifier.weight(1f)) {
                        OutlinedTextField(value = currency, onValueChange = {}, readOnly = true, label = { Text("العملة") }, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedCurrency) }, modifier = Modifier.menuAnchor())
                        ExposedDropdownMenu(expanded = expandedCurrency, onDismissRequest = { expandedCurrency = false }) {
                            listOf("YER", "SAR", "USD").forEach { cur ->
                                DropdownMenuItem(text = { Text(cur) }, onClick = { currency = cur; expandedCurrency = false })
                            }
                        }
                    }
                }
                
                OutlinedTextField(value = category, onValueChange = { category = it }, label = { Text("التصنيف") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = usage, onValueChange = { usage = it }, label = { Text("طريقة الاستخدام") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = warnings, onValueChange = { warnings = it }, label = { Text("التحذيرات") }, modifier = Modifier.fillMaxWidth())
                
                Button(
                    onClick = { imagePickerLauncher.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isUploading
                ) {
                    Text(if (isUploading) "جاري الرفع..." else "اختيار صورة")
                }
                
                if (imageUrl.isNotEmpty()) {
                    Text("تم رفع الصورة بنجاح", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium)
                }
            }
        },
        confirmButton = {
            Button(onClick = {
                onSave(product.copy(
                    name = name,
                    price = priceStr.toDoubleOrNull() ?: 0.0,
                    description = description,
                    usage = usage,
                    warnings = warnings,
                    category = category,
                    currency = currency,
                    imageUrl = imageUrl
                ))
            }, enabled = !isUploading) { Text("حفظ") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("إلغاء") }
        }
    )
}
@Composable
fun CropDialog(crop: Crop, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Crop) -> Unit) {
    var name by remember { mutableStateOf(crop.name) }
    var synonymsStr by remember { mutableStateOf(crop.synonyms.joinToString(", ")) }
    var description by remember { mutableStateOf(crop.description) }
    var plantingSeason by remember { mutableStateOf(crop.plantingSeason) }
    var soil by remember { mutableStateOf(crop.soil) }
    var irrigation by remember { mutableStateOf(crop.irrigation) }
    var fertilization by remember { mutableStateOf(crop.fertilization) }
    var notes by remember { mutableStateOf(crop.notes) }
    var isActive by remember { mutableStateOf(crop.isActive) }
    var isSaving by remember { mutableStateOf(false) }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة محصول جديد" else "تعديل المحصول") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.verticalScroll(rememberScrollState())) {
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("الاسم") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = synonymsStr, onValueChange = { synonymsStr = it }, label = { Text("المرادفات (مفصولة بفاصلة)") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = description, onValueChange = { description = it }, label = { Text("الوصف") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = plantingSeason, onValueChange = { plantingSeason = it }, label = { Text("موسم الزراعة") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = soil, onValueChange = { soil = it }, label = { Text("التربة المناسبة") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = irrigation, onValueChange = { irrigation = it }, label = { Text("إرشادات الري") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = fertilization, onValueChange = { fertilization = it }, label = { Text("إرشادات التسميد") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = notes, onValueChange = { notes = it }, label = { Text("ملاحظات") }, modifier = Modifier.fillMaxWidth())
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Switch(checked = isActive, onCheckedChange = { isActive = it })
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("نشط", style = MaterialTheme.typography.bodyMedium)
                }
            }
        },
        confirmButton = {
            Button(
                enabled = !isSaving,
                onClick = { 
                    isSaving = true
                    val synonyms = synonymsStr.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                    onSave(crop.copy(
                        name = name, 
                        synonyms = synonyms,
                        description = description,
                        plantingSeason = plantingSeason,
                        soil = soil,
                        irrigation = irrigation,
                        fertilization = fertilization,
                        notes = notes,
                        isActive = isActive
                    )) 
                }
            ) { Text("حفظ") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss, enabled = !isSaving) { Text("إلغاء") }
        }
    )
}
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProblemDialog(
    problem: AgriculturalProblem, 
    crops: List<Crop>, 
    products: List<Product>,
    isAdding: Boolean, 
    onDismiss: () -> Unit, 
    onSave: (AgriculturalProblem) -> Unit
) {
    var name by remember { mutableStateOf(problem.name) }
    var synonymsStr by remember { mutableStateOf(problem.synonyms.joinToString(", ")) }
    var cropId by remember { mutableStateOf(problem.cropId) }
    var type by remember { mutableStateOf(problem.type) }
    var symptomsStr by remember { mutableStateOf(problem.symptoms.joinToString(", ")) }
    var causes by remember { mutableStateOf(problem.causes) }
    var prevention by remember { mutableStateOf(problem.prevention) }
    var treatment by remember { mutableStateOf(problem.treatment) }
    var selectedProductIds by remember { mutableStateOf(problem.recommendedProductIds.toSet()) }
    var isActive by remember { mutableStateOf(problem.isActive) }
    var isSaving by remember { mutableStateOf(false) }
    
    var expandedCrop by remember { mutableStateOf(false) }
    var expandedType by remember { mutableStateOf(false) }
    
    val scrollState = rememberScrollState()
    val types = listOf("disease", "pest", "deficiency", "other")

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة مشكلة جديدة" else "تعديل مشكلة", fontWeight = FontWeight.Bold) },
        text = {
            Column(
                modifier = Modifier.verticalScroll(scrollState),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                ExposedDropdownMenuBox(
                    expanded = expandedCrop,
                    onExpandedChange = { expandedCrop = !expandedCrop }
                ) {
                    val selectedCropName = crops.find { it.id == cropId }?.name ?: "اختر المحصول"
                    OutlinedTextField(
                        value = selectedCropName,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("المحصول") },
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable).fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp)
                    )
                    ExposedDropdownMenu(expanded = expandedCrop, onDismissRequest = { expandedCrop = false }) {
                        crops.forEach { c ->
                            DropdownMenuItem(
                                text = { Text(c.name) },
                                onClick = { cropId = c.id; expandedCrop = false }
                            )
                        }
                    }
                }
                
                OutlinedTextField(
                    value = name, 
                    onValueChange = { name = it }, 
                    label = { Text("اسم المشكلة") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                OutlinedTextField(
                    value = synonymsStr, 
                    onValueChange = { synonymsStr = it }, 
                    label = { Text("المرادفات (مفصولة بفاصلة)") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                ExposedDropdownMenuBox(
                    expanded = expandedType,
                    onExpandedChange = { expandedType = !expandedType }
                ) {
                    OutlinedTextField(
                        value = type.ifEmpty { "اختر النوع" },
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("النوع") },
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable).fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp)
                    )
                    ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                        types.forEach { t ->
                            DropdownMenuItem(
                                text = { Text(t) },
                                onClick = { type = t; expandedType = false }
                            )
                        }
                    }
                }
                
                OutlinedTextField(
                    value = symptomsStr, 
                    onValueChange = { symptomsStr = it }, 
                    label = { Text("الأعراض (مفصولة بفاصلة)") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                OutlinedTextField(
                    value = causes, 
                    onValueChange = { causes = it }, 
                    label = { Text("الأسباب") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )

                OutlinedTextField(
                    value = prevention, 
                    onValueChange = { prevention = it }, 
                    label = { Text("طرق الوقاية") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                OutlinedTextField(
                    value = treatment, 
                    onValueChange = { treatment = it }, 
                    label = { Text("العلاج") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                
                Text("المنتجات المرتبطة:", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    products.forEach { p ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(
                                checked = selectedProductIds.contains(p.id),
                                onCheckedChange = { checked -> 
                                    val newSet = selectedProductIds.toMutableSet()
                                    if (checked) newSet.add(p.id) else newSet.remove(p.id)
                                    selectedProductIds = newSet
                                }
                            )
                            Text(p.name, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Switch(checked = isActive, onCheckedChange = { isActive = it })
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("نشط", style = MaterialTheme.typography.bodyMedium)
                }
            }
        },
        confirmButton = {
            Button(
                enabled = !isSaving,
                onClick = {
                    isSaving = true
                    val symptoms = symptomsStr.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                    val synonyms = synonymsStr.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                    onSave(problem.copy(
                        name = name, cropId = cropId, type = type, 
                        synonyms = synonyms, prevention = prevention,
                        symptoms = symptoms, causes = causes, treatment = treatment,
                        recommendedProductIds = selectedProductIds.toList(), isActive = isActive
                    ))
                }
            ) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !isSaving) { Text("إلغاء") } },
        shape = RoundedCornerShape(24.dp)
    )
}
