import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Fix CropsList signature
content = content.replace("fun CropsList(crops: List<Crop>, onEdit: (Crop) -> Unit) {", "fun CropsList(crops: List<Crop>, onEdit: (Crop) -> Unit, onDelete: (Crop) -> Unit) {")

# Fix CropsList row
old_crop_row = """                    }
                    IconButton(onClick = { onEdit(crop) }) {
                        Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                    }
                }"""
new_crop_row = """                    }
                    Row {
                        IconButton(onClick = { onEdit(crop) }) {
                            Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = { onDelete(crop) }) {
                            Icon(Icons.Outlined.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""
content = content.replace(old_crop_row, new_crop_row)


# Fix ProblemsList signature
content = content.replace("fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit) {", "fun ProblemsList(problems: List<AgriculturalProblem>, crops: List<Crop>, onEdit: (AgriculturalProblem) -> Unit, onDelete: (AgriculturalProblem) -> Unit) {")

# Fix ProblemsList row
old_prob_row = """                    }
                    IconButton(onClick = { onEdit(problem) }) {
                        Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                    }
                }"""
new_prob_row = """                    }
                    Row {
                        IconButton(onClick = { onEdit(problem) }) {
                            Icon(Icons.Outlined.Edit, contentDescription = "تعديل", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = { onDelete(problem) }) {
                            Icon(Icons.Outlined.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""
content = content.replace(old_prob_row, new_prob_row)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

