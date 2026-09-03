import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Remove AnimatedVisibility from CropCard
crop_anim_pattern = re.compile(r'            AnimatedVisibility\([^)]+\)\s*\{\s*Column\([^)]+\)\s*\{[^\}]+\}\s*\}\s*\}\s*\}', re.DOTALL)
# Actually it's easier to just do string replacement
crop_expanded_old = """                    Icon(if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                }
            }
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = tween(300)),
                exit = shrinkVertically(animationSpec = tween(300))
            ) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    if (crop.description.isNotEmpty()) DetailSection("الوصف", crop.description)
                    if (crop.plantingSeason.isNotEmpty()) DetailSection("موسم الزراعة", crop.plantingSeason)
                    if (crop.soil.isNotEmpty()) DetailSection("التربة المناسبة", crop.soil)
                    if (crop.irrigation.isNotEmpty()) DetailSection("إرشادات الري", crop.irrigation)
                    if (crop.fertilization.isNotEmpty()) DetailSection("إرشادات التسميد", crop.fertilization)
                    if (crop.notes.isNotEmpty()) DetailSection("ملاحظات هامة", crop.notes)
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(
                        onClick = {
                            scope.launch {
                                if (isMyCrop) {
                                    if (userServicesRepository.removeMyCrop(crop.id).isSuccess) {
                                        isMyCrop = false
                                        Toast.makeText(context, "تمت الإزالة من محاصيلي", Toast.LENGTH_SHORT).show()
                                    }
                                } else {
                                    if (userServicesRepository.addMyCrop(crop.id).isSuccess) {
                                        isMyCrop = true
                                        Toast.makeText(context, "تمت الإضافة لمحاصيلي", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = if (isMyCrop) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(if (isMyCrop) Icons.Filled.Check else Icons.Filled.Add, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (isMyCrop) "مضاف إلى محاصيلي" else "أضف إلى محاصيلي")
                    }
                }
            }"""

crop_expanded_new = """                }
            }"""
content = content.replace(crop_expanded_old, crop_expanded_new)

# Remove AnimatedVisibility from ProblemCard
problem_expanded_old = """                    Icon(if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore, contentDescription = null, tint = MaterialTheme.colorScheme.onErrorContainer)
                }
            }
            Text(problem.type, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))
            
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = tween(300)),
                exit = shrinkVertically(animationSpec = tween(300))
            ) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    if (problem.symptoms.isNotEmpty()) DetailSection("الأعراض", problem.symptoms.joinToString("، "))
                    if (problem.causes.isNotEmpty()) DetailSection("الأسباب", problem.causes)
                    if (problem.prevention.isNotEmpty()) DetailSection("طرق الوقاية", problem.prevention)
                    if (problem.treatment.isNotEmpty()) DetailSection("العلاج", problem.treatment)
                }
            }"""

problem_expanded_new = """                }
            }
            Text(problem.type, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))"""
content = content.replace(problem_expanded_old, problem_expanded_new)

# Clean up variables inside the cards
content = content.replace('    var expanded by remember { mutableStateOf(false) }\n', '')

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
