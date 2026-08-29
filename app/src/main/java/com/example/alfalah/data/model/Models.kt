package com.example.alfalah.data.model

import com.google.firebase.firestore.DocumentId
import com.squareup.moshi.JsonClass

data class User(
    @DocumentId val id: String = "",
    val name: String = "",
    val email: String = "",
    val role: String = "user" // "user" or "admin"
)

data class Product(
    @DocumentId val id: String = "",
    val name: String = "",
    val imageUrl: String = "",
    val description: String = "",
    val price: Double = 0.0,
    val currency: String = "SAR",
    val category: String = "",
    val nutrients: List<String> = emptyList(),
    val suitableCrops: List<String> = emptyList(),
    val suitableProblems: List<String> = emptyList(),
    val usage: String = "",
    val dosage: String = "",
    val warnings: String = "",
    val stock: Int = 0,
    val tested: Boolean = false,
    val recommended: Boolean = false,
    val isActive: Boolean = true
)

data class Crop(
    @DocumentId val id: String = "",
    val name: String = "",
    val synonyms: List<String> = emptyList(),
    val description: String = "",
    val isActive: Boolean = true
)

data class AgriculturalProblem(
    @DocumentId val id: String = "",
    val cropId: String = "",
    val name: String = "",
    val synonyms: List<String> = emptyList(),
    val type: String = "",
    val symptoms: List<String> = emptyList(),
    val causes: String = "",
    val prevention: String = "",
    val treatment: String = "",
    val recommendedProductIds: List<String> = emptyList(),
    val isActive: Boolean = true
)

data class ChatMessage(
    val id: String = "",
    val text: String = "",
    val isUser: Boolean = true,
    val timestamp: Long = System.currentTimeMillis(),
    val recommendedProductIds: List<String> = emptyList()
)

// Custom Backend API Models
@JsonClass(generateAdapter = true)
data class AiChatRequest(
    val message: String,
    val conversationId: String = ""
)

@JsonClass(generateAdapter = true)
data class AiChatResponse(
    val answer: String,
    val recommendedProducts: List<String> = emptyList()
)
