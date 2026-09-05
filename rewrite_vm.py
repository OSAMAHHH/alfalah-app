import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

bad_block = """            try {
                val cropsResult = firestoreRepository.getCrops().getOrNull() ?: emptyList()
                val problemsResult = firestoreRepository.getProblems().getOrNull() ?: emptyList()
                
                val lowerText = text.lowercase()
                val matchedCrops = cropsResult.filter { crop -> 
                    lowerText.contains(crop.name.lowercase()) || (crop.synonyms.any { lowerText.contains(it.lowercase()) })
                }
                
                val matchedProblems = problemsResult.filter { problem -> 
                    lowerText.contains(problem.name.lowercase()) || (problem.synonyms.any { lowerText.contains(it.lowercase()) })
                }
                
                if (matchedCrops.isNotEmpty() || matchedProblems.isNotEmpty()) {
                    contextText = "معلومات من قاعدة بيانات التطبيق:"
                    matchedCrops.forEach { c -> 
                        contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}"
                    }
                    contextText += "بناءً على ذلك، أجب عن: "
                }
            } catch (e: Exception) {
            }"""

good_block = """            try {
                val cropsResult = firestoreRepository.getCrops().getOrNull() ?: emptyList()
                val problemsResult = firestoreRepository.getProblems().getOrNull() ?: emptyList()
                
                val lowerText = text.lowercase()
                val matchedCrops = cropsResult.filter { crop -> 
                    lowerText.contains(crop.name.lowercase()) || (crop.synonyms.any { lowerText.contains(it.lowercase()) })
                }
                
                val matchedProblems = problemsResult.filter { problem -> 
                    lowerText.contains(problem.name.lowercase()) || (problem.synonyms.any { lowerText.contains(it.lowercase()) })
                }
                
                if (matchedCrops.isNotEmpty() || matchedProblems.isNotEmpty()) {
                    contextText = "معلومات من قاعدة بيانات التطبيق:\\n"
                    matchedCrops.forEach { c -> 
                        contextText += "المحصول: " + c.name + " - الزراعة: " + c.plantingSeason + " - الري: " + c.wateringSchedule + "\\n"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة: " + p.name + " - الأعراض: " + p.symptoms.toString() + " - العلاج: " + p.treatment + "\\n"
                    }
                    contextText += "\\nبناءً على ذلك، أجب عن: "
                }
            } catch (e: Exception) {
            }"""

content = content.replace(bad_block, good_block)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)

