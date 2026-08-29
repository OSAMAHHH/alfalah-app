import os

content = """package com.example.alfalah.ui.screens.admin

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
import com.example.alfalah.data.model.AgriculturalProblem
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.FirestoreRepository
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdminDashboardScreen(
    onBack: () -> Unit,
    modifier: Modifier = Modifier,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("المنتجات", "المحاصيل", "المشاكل")
    
    var products by remember { mutableStateOf<List<Product>>(emptyList()) }
    var crops by remember { mutableStateOf<List<Crop>>(emptyList()) }
    var problems by remember { mutableStateOf<List<AgriculturalProblem>>(emptyList()) }
    
    var isLoading by remember { mutableStateOf(true) }
    val scope = rememberCoroutineScope()

    var showProductDialog by remember { mutableStateOf<Product?>(null) }
    var showCropDialog by remember { mutableStateOf<Crop?>(null) }
    var showProblemDialog by remember { mutableStateOf<AgriculturalProblem?>(null) }
    var isAdding by remember { mutableStateOf(false) }

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
                    title = { Text("لوحة تحكم المشرف", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.background
                    )
                )
                TabRow(
                    selectedTabIndex = selectedTab,
                    containerColor = MaterialTheme.colorScheme.background,
                    contentColor = MaterialTheme.colorScheme.primary
                ) {
                    tabs.forEachIndexed { index, title ->
                        Tab(
                            selected = selectedTab == index,
                            onClick = { selectedTab = index },
                            text = { 
                                Text(
                                    title, 
                                    fontWeight = if (selectedTab == index) FontWeight.Bold else FontWeight.Normal
                                ) 
                            }
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
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center),
                    color = MaterialTheme.colorScheme.primary
                )
            } else {
                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false })
                }
            }
        }

        if (showProductDialog != null) {
            ProductDialog(
                product = showProductDialog!!,
                isAdding = isAdding,
                onDismiss = { showProductDialog = null },
                onSave = { p ->
                    scope.launch {
                        if (isAdding) firestoreRepository.addProduct(p) else firestoreRepository.updateProduct(p)
                        showProductDialog = null
                        loadData()
                    }
                }
            )
        }
        
        if (showCropDialog != null) {
            CropDialog(
                crop = showCropDialog!!,
                isAdding = isAdding,
                onDismiss = { showCropDialog = null },
                onSave = { c ->
                    scope.launch {
                        if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        showCropDialog = null
                        loadData()
                    }
                }
            )
        }

        if (showProblemDialog != null) {
            ProblemDialog(
                problem = showProblemDialog!!,
                crops = crops,
                products = products,
                isAdding = isAdding,
                onDismiss = { showProblemDialog = null },
                onSave = { pr ->
                    scope.launch {
                        if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        showProblemDialog = null
                        loadData()
                    }
                }
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
                            "السعر: ${product.price} ر.س", 
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
fun CropsList(crops: List<Crop>, onEdit: (Crop) -> Unit) {
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
                    IconButton(onClick = { onEdit(crop) }) {
                        Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    }
}

@Composable
fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit) {
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
                    IconButton(onClick = { onEdit(problem) }) {
                        Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
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

@Composable
fun ProductDialog(product: Product, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Product) -> Unit) {
    var name by remember { mutableStateOf(product.name) }
    var priceStr by remember { mutableStateOf(if (product.price == 0.0) "" else product.price.toString()) }
    var usage by remember { mutableStateOf(product.usage) }
    var isActive by remember { mutableStateOf(product.isActive) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة منتج جديد" else "تعديل منتج", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name, 
                    onValueChange = { name = it }, 
                    label = { Text("اسم المنتج") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                OutlinedTextField(
                    value = priceStr, 
                    onValueChange = { priceStr = it }, 
                    label = { Text("السعر") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                OutlinedTextField(
                    value = usage, 
                    onValueChange = { usage = it }, 
                    label = { Text("الاستخدام") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Switch(checked = isActive, onCheckedChange = { isActive = it })
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("نشط", style = MaterialTheme.typography.bodyMedium)
                }
            }
        },
        confirmButton = {
            Button(onClick = {
                onSave(product.copy(
                    name = name,
                    price = priceStr.toDoubleOrNull() ?: 0.0,
                    usage = usage,
                    isActive = isActive
                ))
            }) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } },
        shape = RoundedCornerShape(24.dp)
    )
}

@Composable
fun CropDialog(crop: Crop, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Crop) -> Unit) {
    var name by remember { mutableStateOf(crop.name) }
    var synonymsStr by remember { mutableStateOf(crop.synonyms.joinToString(", ")) }
    var isActive by remember { mutableStateOf(crop.isActive) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة محصول جديد" else "تعديل محصول", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name, 
                    onValueChange = { name = it }, 
                    label = { Text("اسم المحصول") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                OutlinedTextField(
                    value = synonymsStr, 
                    onValueChange = { synonymsStr = it }, 
                    label = { Text("مرادفات (مفصولة بفاصلة)") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Switch(checked = isActive, onCheckedChange = { isActive = it })
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("نشط", style = MaterialTheme.typography.bodyMedium)
                }
            }
        },
        confirmButton = {
            Button(onClick = {
                val synonyms = synonymsStr.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                onSave(crop.copy(name = name, synonyms = synonyms, isActive = isActive))
            }) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } },
        shape = RoundedCornerShape(24.dp)
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
    var cropId by remember { mutableStateOf(problem.cropId) }
    var type by remember { mutableStateOf(problem.type) }
    var symptomsStr by remember { mutableStateOf(problem.symptoms.joinToString(", ")) }
    var causes by remember { mutableStateOf(problem.causes) }
    var treatment by remember { mutableStateOf(problem.treatment) }
    var selectedProductIds by remember { mutableStateOf(problem.recommendedProductIds.toSet()) }
    var isActive by remember { mutableStateOf(problem.isActive) }
    
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
                // Crop Selection
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
                
                // Type Selection
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
            Button(onClick = {
                val symptoms = symptomsStr.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                onSave(problem.copy(
                    name = name, cropId = cropId, type = type, 
                    symptoms = symptoms, causes = causes, treatment = treatment,
                    recommendedProductIds = selectedProductIds.toList(), isActive = isActive
                ))
            }) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } },
        shape = RoundedCornerShape(24.dp)
    )
}
"""

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)

