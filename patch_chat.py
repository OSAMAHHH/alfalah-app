import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    text = f.read()

new_send_message = """
    fun sendMessage(text: String) {
        if (text.isBlank()) return
        
        val userMsg = ChatMessageUi(
            id = System.currentTimeMillis().toString(),
            text = text,
            isUser = true
        )
        _messages.value = _messages.value + userMsg
        
        _isLoading.value = true
        
        viewModelScope.launch {
            // Local Knowledge Base Search First
            val localResponse = searchLocalKnowledgeBase(text)
            if (localResponse != null) {
                val aiMsg = ChatMessageUi(
                    id = (System.currentTimeMillis() + 1).toString(),
                    text = localResponse,
                    isUser = false,
                    recommendedProducts = emptyList() // Could enrich later
                )
                _messages.value = _messages.value + aiMsg
                _isLoading.value = false
                return@launch
            }

            // Fallback to Gemini Backend
            val (responseText, productIds) = aiRepository.askAssistant(text)
            
            // Handle exhaustion gracefully
            var finalResponseText = responseText
            if (responseText.contains("تجاوزت حد الاستخدام") || responseText.contains("غير متاحة مؤقتاً") || responseText.contains("لا يمكنني الاتصال")) {
                finalResponseText = "المساعد الذكي غير متاح مؤقتاً، لكن يمكنك الاستفادة من دليل المزارع الآن."
            }
            
            val recommendedProducts = mutableListOf<Product>()
            for (id in productIds) {
                val p = firestoreRepository.getProductById(id).getOrNull()
                if (p != null) {
                    recommendedProducts.add(p)
                }
            }
            
            val aiMsg = ChatMessageUi(
                id = (System.currentTimeMillis() + 1).toString(),
                text = finalResponseText,
                isUser = false,
                recommendedProducts = recommendedProducts
            )
            
            _messages.value = _messages.value + aiMsg
            _isLoading.value = false
        }
    }

    private suspend fun searchLocalKnowledgeBase(query: String): String? {
        val problems = firestoreRepository.getProblems().getOrNull() ?: emptyList()
        val crops = firestoreRepository.getCrops().getOrNull() ?: emptyList()
        
        // Very basic semantic matching based on keywords
        val lowerQuery = query.lowercase()
        
        // 1. Check for specific problems/diseases
        for (problem in problems) {
            val hasName = lowerQuery.contains(problem.name.lowercase())
            val hasSynonym = problem.synonyms.any { lowerQuery.contains(it.lowercase()) }
            if (hasName || hasSynonym) {
                val cropName = crops.find { it.id == problem.cropId }?.name ?: "المحصول"
                return "من خلال قاعدة المعرفة (دليل المزارع):\\n" +
                       "المشكلة: ${problem.name} في $cropName\\n" +
                       "الأعراض: ${problem.symptoms.joinToString("، ")}\\n" +
                       "الأسباب: ${problem.causes}\\n" +
                       "العلاج: ${problem.treatment}"
            }
        }
        
        // 2. Check for general crop info
        for (crop in crops) {
            val hasName = lowerQuery.contains(crop.name.lowercase())
            val hasSynonym = crop.synonyms.any { lowerQuery.contains(it.lowercase()) }
            
            if (hasName || hasSynonym) {
                // If they ask a general question about the crop
                if (lowerQuery.contains("معلومات") || lowerQuery.contains("ما هو") || lowerQuery.contains("زراعة")) {
                    return "من خلال قاعدة المعرفة (دليل المزارع):\\n" +
                           "المحصول: ${crop.name}\\n" +
                           "الوصف: ${crop.description}\\n"
                }
            }
        }
        
        return null // Not found locally, proceed to Gemini
    }
"""

text = re.sub(r'fun sendMessage\(text: String\) \{[\s\S]*?\}\s*\}', new_send_message + '\n}', text)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(text)
