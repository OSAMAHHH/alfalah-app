import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Update CropDialog
old_crop_dialog = """fun CropDialog(crop: Crop, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Crop) -> Unit) {
    var name by remember { mutableStateOf(crop.name) }
    var description by remember { mutableStateOf(crop.description) }
    var plantingSeason by remember { mutableStateOf(crop.plantingSeason) }
    var soil by remember { mutableStateOf(crop.soil) }
    var irrigation by remember { mutableStateOf(crop.irrigation) }
    var fertilization by remember { mutableStateOf(crop.fertilization) }
    var notes by remember { mutableStateOf(crop.notes) }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (isAdding) "إضافة محصول جديد" else "تعديل المحصول") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.verticalScroll(rememberScrollState())) {
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("الاسم") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = description, onValueChange = { description = it }, label = { Text("الوصف") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = plantingSeason, onValueChange = { plantingSeason = it }, label = { Text("موسم الزراعة") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = soil, onValueChange = { soil = it }, label = { Text("التربة المناسبة") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = irrigation, onValueChange = { irrigation = it }, label = { Text("إرشادات الري") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = fertilization, onValueChange = { fertilization = it }, label = { Text("إرشادات التسميد") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = notes, onValueChange = { notes = it }, label = { Text("ملاحظات") }, modifier = Modifier.fillMaxWidth())
            }
        },
        confirmButton = {
            Button(onClick = { onSave(crop.copy(
                name = name, 
                description = description,
                plantingSeason = plantingSeason,
                soil = soil,
                irrigation = irrigation,
                fertilization = fertilization,
                notes = notes
            )) }) { Text("حفظ") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("إلغاء") }
        }
    )
}"""

new_crop_dialog = """fun CropDialog(crop: Crop, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Crop) -> Unit) {
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
}"""

content = content.replace(old_crop_dialog, new_crop_dialog)

# Update ProblemDialog (replace from start of ProblemDialog to end)
# Since the length of ProblemDialog is larger, we use regex.
old_problem_dialog_pattern = r"@OptIn\(ExperimentalMaterial3Api::class\)\s*@Composable\s*fun ProblemDialog\(.*?\}\s*\)\s*\}"

new_problem_dialog = """@OptIn(ExperimentalMaterial3Api::class)
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
}"""

content = re.sub(old_problem_dialog_pattern, new_problem_dialog, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

