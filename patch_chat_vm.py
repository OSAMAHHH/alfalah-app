import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

rag_logic = """
            var contextText = ""
            try {
                // RAG: Fetch local knowledge base to inject context if relevant
                val cropsResult = firestoreRepository.getCrops().getOrNull() ?: emptyList()
                val problemsResult = firestoreRepository.getProblems().getOrNull() ?: emptyList()
                
                val matchedCrops = cropsResult.filter { crop -> 
                    text.contains(crop.name) || crop.synonyms.any { text.contains(it) }
                }
                
                val matchedProblems = problemsResult.filter { problem -> 
                    text.contains(problem.name) || problem.synonyms.any { text.contains(it) }
                }
                
                if (matchedCrops.isNotEmpty() || matchedProblems.isNotEmpty()) {
                    contextText = "معلومات من قاعدة بيانات التطبيق (استخدمها للإجابة إذا كانت ذات صلة):\\n"
                    matchedCrops.forEach { c -> 
                        contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\n"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة/الآفة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}\\n"
                    }
                    contextText += "\\nسؤال المستخدم: "
                }
            } catch (e: Exception) {
                // Ignore errors and proceed without context
            }
            
            val finalPrompt = if (contextText.isEmpty()) text else contextText + text
            val (responseText, productIds) = aiRepository.askAssistant(finalPrompt, historyItems)
"""

# replace the block
old_block = """            var contextText = ""
            try {
                // val myCrops = userServicesRepository.getMyCrops()
                // ... we can just ignore contextText for now or add empty ...
            } catch (e: Exception) {}
            val historyItems = _messages.value.takeLast(5).map { msg ->
                ChatMessageItem(
                    role = if (msg.isUser) "user" else "assistant",
                    content = msg.text
                )
            }
            val (responseText, productIds) = aiRepository.askAssistant(contextText + text, historyItems)"""

new_block = """            val historyItems = _messages.value.takeLast(5).map { msg ->
                ChatMessageItem(
                    role = if (msg.isUser) "user" else "assistant",
                    content = msg.text
                )
            }
""" + rag_logic

content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
