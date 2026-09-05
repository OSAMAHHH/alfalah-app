package com.example.alfalah.ui.screens.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.alfalah.data.model.*
import com.example.alfalah.data.repository.AiRepository
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class ChatMessageUi(
    val id: String = "",
    val text: String = "",
    val isUser: Boolean = true,
    val recommendedProducts: List<Product> = emptyList()
)

class ChatViewModel(
    private val aiRepository: AiRepository = AiRepository(),
    private val firestoreRepository: FirestoreRepository = FirestoreRepository(),
    private val userServicesRepository: UserServicesRepository = UserServicesRepository()
) : ViewModel() {
    private var currentConversationId: String? = null
    private var currentConversation: Conversation? = null

    private val _messages = MutableStateFlow<List<ChatMessageUi>>(emptyList())
    val messages: StateFlow<List<ChatMessageUi>> = _messages.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    fun loadConversation(id: String?) {
        if (id.isNullOrEmpty()) {
            currentConversationId = null
            currentConversation = null
            _messages.value = emptyList()
            return
        }
        currentConversationId = id
        viewModelScope.launch {
            _isLoading.value = true
            val conversations = userServicesRepository.getConversations()
            currentConversation = conversations.find { it.id == id }
            if (currentConversation != null) {
                _messages.value = currentConversation!!.messages.map { 
                    ChatMessageUi(id = it.id, text = it.text, isUser = it.isUser)
                }
            } else {
                _messages.value = emptyList()
            }
            _isLoading.value = false
        }
    }

    fun sendMessage(text: String) {
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
                    contextText = "معلومات من قاعدة بيانات التطبيق:\n"
                    matchedCrops.forEach { c -> 
                        contextText += "المحصول: " + c.name + " - الزراعة: " + c.plantingSeason + "\n"
                    }
                    matchedProblems.forEach { p ->
                        contextText += "المشكلة: " + p.name + " - العلاج: " + p.treatment + "\n"
                    }
                    contextText += "\nبناءً على ذلك، أجب عن: "
                }
            } catch (e: Exception) {
            }
            
            val finalPrompt = if (contextText.isEmpty()) text else contextText + text
            val (responseText, productIds) = aiRepository.askAssistant(finalPrompt, historyItems)

            val recommendedProducts = mutableListOf<Product>()
            for (pid in productIds) {
                val p = firestoreRepository.getProductById(pid).getOrNull()
                if (p != null) recommendedProducts.add(p)
            }
            
            val aiMsg = ChatMessageUi(
                id = (System.currentTimeMillis() + 1).toString(),
                text = responseText,
                isUser = false,
                recommendedProducts = recommendedProducts
            )
            
            _messages.value = _messages.value + aiMsg
            _isLoading.value = false

            // Save conversation
            val chatMessages = _messages.value.map { 
                ChatMessage(id = it.id, text = it.text, isUser = it.isUser, timestamp = System.currentTimeMillis())
            }
            val title = if (currentConversation?.title.isNullOrEmpty()) {
                if (text.length > 20) text.substring(0, 20) + "..." else text
            } else currentConversation!!.title

            val conv = Conversation(
                id = currentConversationId ?: "",
                title = title,
                updatedAt = System.currentTimeMillis(),
                messages = chatMessages
            )
            // val saveResult = userServicesRepository.saveConversation(conv)
        }
    }
}
