package com.example.alfalah.ui.screens.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.alfalah.data.model.ChatMessage
import com.example.alfalah.data.model.Product
import com.example.alfalah.data.repository.AiRepository
import com.example.alfalah.data.repository.FirestoreRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

// Wrapper for UI state
data class ChatMessageUi(
    val id: String,
    val text: String,
    val isUser: Boolean,
    val recommendedProducts: List<Product> = emptyList()
)

class ChatViewModel(
    private val aiRepository: AiRepository = AiRepository(),
    private val firestoreRepository: FirestoreRepository = FirestoreRepository()
) : ViewModel() {

    private val _messages = MutableStateFlow<List<ChatMessageUi>>(emptyList())
    val messages: StateFlow<List<ChatMessageUi>> = _messages.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

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
            // Note: Sending empty conversationId for MVP. Real app would maintain conversation state.
            val (responseText, productIds) = aiRepository.askAssistant(text)
            
            // Resolve product IDs into actual Product objects for the UI
            val recommendedProducts = mutableListOf<Product>()
            for (id in productIds) {
                val p = firestoreRepository.getProductById(id).getOrNull()
                if (p != null) {
                    recommendedProducts.add(p)
                }
            }
            
            val aiMsg = ChatMessageUi(
                id = (System.currentTimeMillis() + 1).toString(),
                text = responseText,
                isUser = false,
                recommendedProducts = recommendedProducts
            )
            
            _messages.value = _messages.value + aiMsg
            _isLoading.value = false
        }
    }
}
