with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CropsList
old_crops_list = """@Composable
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
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            crop.plantingSeason, 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        StatusBadge(isActive = crop.isActive)
                    }
                    IconButton(onClick = { onEdit(crop) }) {
                        Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    }
}"""

new_crops_list = """@Composable
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
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            crop.plantingSeason, 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(4.dp))
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
}"""

content = content.replace(old_crops_list, new_crops_list)

# 2. Update ProblemsList
old_problems_list = """@Composable
fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit) {
    if (problems.isEmpty()) {
        EmptyStateMessage("لا توجد مشاكل")
        return
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(problems) { problem ->
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
                        val cropName = crops.find { it.id == problem.cropId }?.name ?: "غير معروف"
                        Text(
                            "المحصول: $cropName", 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.primary
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
}"""

new_problems_list = """@Composable
fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit, onDelete: (AgriculturalProblem) -> Unit) {
    if (problems.isEmpty()) {
        EmptyStateMessage("لا توجد مشاكل")
        return
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(problems) { problem ->
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
                        val cropName = crops.find { it.id == problem.cropId }?.name ?: "غير معروف"
                        Text(
                            "المحصول: $cropName", 
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.primary
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
}"""

content = content.replace(old_problems_list, new_problems_list)

# 3. Add Dialogs and state
state_declarations_old = """    var isAdding by remember { mutableStateOf(false) }"""
state_declarations_new = """    var isAdding by remember { mutableStateOf(false) }
    var cropToDelete by remember { mutableStateOf<Crop?>(null) }
    var problemToDelete by remember { mutableStateOf<AgriculturalProblem?>(null) }"""

content = content.replace(state_declarations_old, state_declarations_new)

calls_old = """                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false })
                }"""
calls_new = """                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false }, { c -> cropToDelete = c })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false }, { pr -> problemToDelete = pr })
                }"""
content = content.replace(calls_old, calls_new)

delete_dialogs = """
        if (cropToDelete != null) {
            AlertDialog(
                onDismissRequest = { cropToDelete = null },
                title = { Text("تأكيد الحذف") },
                text = { Text("هل أنت متأكد أنك تريد حذف المحصول '${cropToDelete!!.name}'؟") },
                confirmButton = {
                    Button(
                        onClick = { 
                            scope.launch {
                                isLoading = true
                                val r = firestoreRepository.deleteCrop(cropToDelete!!.id)
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
                text = { Text("هل أنت متأكد أنك تريد حذف المشكلة '${problemToDelete!!.name}'؟") },
                confirmButton = {
                    Button(
                        onClick = { 
                            scope.launch {
                                isLoading = true
                                val r = firestoreRepository.deleteProblem(problemToDelete!!.id)
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
"""
import re
content = re.sub(r'    }\n}\n\n@Composable\nfun ProductsList', delete_dialogs + '    }\n}\n\n@Composable\nfun ProductsList', content)

# 4. Add Toasts to existing onSave functions
old_crop_save = """val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        showCropDialog = null"""
new_crop_save = """val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المحصول بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showCropDialog = null"""
content = content.replace(old_crop_save, new_crop_save)

old_problem_save = """val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        showProblemDialog = null"""
new_problem_save = """val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المشكلة بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showProblemDialog = null"""
content = content.replace(old_problem_save, new_problem_save)


# 5. Extract original CropDialog and ProblemDialog strings
import sys
# We know CropDialog starts at `fun CropDialog` and ends at `}` before `@OptIn`
crop_start = content.find("fun CropDialog(")
crop_end = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ProblemDialog")
if crop_start == -1 or crop_end == -1:
    print("Failed to find crop bounds")
    sys.exit(1)

old_crop_dialog = content[crop_start:crop_end]

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
}
"""

content = content.replace(old_crop_dialog, new_crop_dialog)

prob_start = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ProblemDialog")
# The rest of the file is ProblemDialog
old_problem_dialog = content[prob_start:]

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
}
"""

content = content.replace(old_problem_dialog, new_problem_dialog)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

