import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

new_crop_dialog = """@Composable
fun CropDialog(crop: Crop, isAdding: Boolean, onDismiss: () -> Unit, onSave: (Crop) -> Unit) {
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

text = re.sub(r'@Composable\s*fun CropDialog\(crop: Crop, isAdding: Boolean, onDismiss: \(\) -> Unit, onSave: \(Crop\) -> Unit\) \{[\s\S]*?(?=@Composable\s*fun ProblemDialog)', new_crop_dialog + "\n\n", text)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
