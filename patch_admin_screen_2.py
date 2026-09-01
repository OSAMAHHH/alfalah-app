import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add states for delete dialogs
state_declarations_old = """    var isAdding by remember { mutableStateOf(false) }"""
state_declarations_new = """    var isAdding by remember { mutableStateOf(false) }
    var cropToDelete by remember { mutableStateOf<Crop?>(null) }
    var problemToDelete by remember { mutableStateOf<AgriculturalProblem?>(null) }"""

content = content.replace(state_declarations_old, state_declarations_new)

# Update the calling logic
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

# Append Delete Dialogs
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
# Insert before the last brace of AdminDashboardScreen
content = re.sub(r'    }\n}\n\n@Composable\nfun ProductsList', delete_dialogs + '    }\n}\n\n@Composable\nfun ProductsList', content)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

