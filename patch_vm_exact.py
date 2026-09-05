import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

# Replace sendMessage function
old_func = """    fun sendMessage(text: String) {
        if (text.isBlank() || _isLoading.value) return
        
        val userMsg = ChatMessageUi(
            id = System.currentTimeMillis().toString(),
            text = text,
            isUser = true
        )
        _messages.value = _messages.value + userMsg
        _isLoading.value = true
        
        viewModelScope.launch {
            // Build context for AI based on MyCrops
            var contextText = ""
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

new_func = """    fun sendMessage(text: String) {
        if (text.isBlank() || _isLoading.value) return
        
        val userMsg = ChatMessageUi(
            id = System.currentTimeMillis().toString(),
            text = text,
            isUser = true
        )
        _messages.value = _messages.value + userMsg
        _isLoading.value = true
        
        viewModelScope.launch {
            val historyItems = _messages.value.takeLast(5).map { msg ->
                ChatMessageItem(
                    role = if (msg.isUser) "user" else "assistant",
                    content = msg.text
                )
            }
            
            var contextText = ""
            try {
                // Fetch local knowledge base to inject context if relevant
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
                    contextText = "معلومات من قاعدة بيانات التطبيق للإجابة الدقيقة:\\n"
                    matchedCrops.forEach { c -> 
                        contextText += "المحصول: ${c.name} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\n"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}\\n"
                    }
                    contextText += "\\nبناءً على ذلك، أجب عن: "
                }
            } catch (e: Exception) {
                // Ignore errors and proceed without context
            }
            
            val finalPrompt = if (contextText.isEmpty()) text else contextText + text
            val (responseText, productIds) = aiRepository.askAssistant(finalPrompt, historyItems)"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find block to replace")
