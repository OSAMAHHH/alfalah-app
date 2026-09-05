import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

pattern = re.compile(
    r'// Build context for AI based on MyCrops.*?val \(responseText, productIds\) = aiRepository\.askAssistant\(contextText \+ text, historyItems\)',
    re.DOTALL
)

new_block = """val historyItems = _messages.value.takeLast(5).map { msg ->
                ChatMessageItem(
                    role = if (msg.isUser) "user" else "assistant",
                    content = msg.text
                )
            }
            
            var contextText = ""
            try {
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
                        contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\n"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}\\n"
                    }
                    contextText += "\\nبناءً على ذلك، أجب عن: "
                }
            } catch (e: Exception) {
            }
            
            val finalPrompt = if (contextText.isEmpty()) text else contextText + text
            val (responseText, productIds) = aiRepository.askAssistant(finalPrompt, historyItems)"""

content = re.sub(pattern, new_block, content)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
