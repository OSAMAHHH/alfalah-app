import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

# Add necessary imports
text = text.replace("import androidx.compose.ui.platform.LocalContext", "import androidx.compose.ui.platform.LocalContext\nimport com.example.alfalah.data.repository.FirestoreRepository\nimport kotlinx.coroutines.launch")

old_dialog = re.search(r'@Composable\s*fun ProductDialog\(product: Product, isAdding: Boolean, onDismiss: \(\) -> Unit, onSave: \(Product\) -> Unit\) \{[\s\S]*?(?=@Composable\s*fun CropDialog)', text).group(0)

new_dialog = """@Composable
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
                            listOf("SAR", "USD", "EGP", "AED").forEach { cur ->
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
"""

text = text.replace(old_dialog, new_dialog)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
