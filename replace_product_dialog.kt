@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductDialog(product: Product, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Product) -> Unit) {
    val context = LocalContext.current
    var name by remember { mutableStateOf(product.name) }
    var priceStr by remember { mutableStateOf(if (product.price == 0.0) "" else product.price.toString()) }
    var usage by remember { mutableStateOf(product.usage) }
    var isActive by remember { mutableStateOf(product.isActive) }
    var currency by remember { mutableStateOf(product.currency.ifEmpty { "SAR" }) }
    var imageUrl by remember { mutableStateOf(product.imageUrl) }
    var expandedCurrency by remember { mutableStateOf(false) }
    
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri: Uri? ->
            if (uri != null) {
                val flag = Intent.FLAG_GRANT_READ_URI_PERMISSION
                context.contentResolver.takePersistableUriPermission(uri, flag)
                imageUrl = uri.toString()
            }
        }
    )

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة منتج جديد" else "تعديل منتج", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = name, onValueChange = { name = it },
                    label = { Text("اسم المنتج") },
                    modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)
                )
                
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = priceStr, onValueChange = { priceStr = it },
                        label = { Text("السعر") },
                        modifier = Modifier.weight(1f), shape = RoundedCornerShape(12.dp)
                    )
                    
                    ExposedDropdownMenuBox(
                        expanded = expandedCurrency,
                        onExpandedChange = { expandedCurrency = !expandedCurrency },
                        modifier = Modifier.weight(1f)
                    ) {
                        OutlinedTextField(
                            value = currency,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("العملة") },
                            modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable).fillMaxWidth(),
                            shape = RoundedCornerShape(12.dp)
                        )
                        ExposedDropdownMenu(expanded = expandedCurrency, onDismissRequest = { expandedCurrency = false }) {
                            listOf("SAR", "USD", "EUR", "EGP").forEach { c ->
                                DropdownMenuItem(text = { Text(c) }, onClick = { currency = c; expandedCurrency = false })
                            }
                        }
                    }
                }
                
                OutlinedTextField(
                    value = usage, onValueChange = { usage = it },
                    label = { Text("الاستخدام") },
                    modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)
                )
                
                Button(
                    onClick = { imagePickerLauncher.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(if (imageUrl.isEmpty()) "اختيار صورة للمنتج" else "تم اختيار الصورة (تغيير)")
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
                onSave(product.copy(name = name, price = priceStr.toDoubleOrNull() ?: 0.0, usage = usage, isActive = isActive, currency = currency, imageUrl = imageUrl))
            }) { Text("حفظ") }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text("إلغاء") } },
        shape = RoundedCornerShape(24.dp)
    )
}
