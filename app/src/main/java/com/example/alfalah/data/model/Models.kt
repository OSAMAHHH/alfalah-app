package com.example.alfalah.data.model

import com.google.firebase.firestore.DocumentId
import com.squareup.moshi.JsonClass
import androidx.annotation.Keep

@Keep
data class User(
    @DocumentId var id: String = "",
    val name: String = "",
    val email: String = "",
    val role: String = "user", // "user" or "admin"
    val photoUrl: String? = null,
    val phone: String = "",
    val governorate: String = "",
    val address: String = ""
)

@JsonClass(generateAdapter = true)
@Keep
data class Product(
    @DocumentId var id: String = "",
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

@JsonClass(generateAdapter = true)
@Keep
data class Crop(
    @DocumentId var id: String = "",
    val name: String = "",
    val synonyms: List<String> = emptyList(),
    val description: String = "",
    val plantingSeason: String = "",
    val soil: String = "",
    val irrigation: String = "",
    val fertilization: String = "",
    val notes: String = "",
    val isActive: Boolean = true
)

@JsonClass(generateAdapter = true)
@Keep
data class AgriculturalProblem(
    @DocumentId var id: String = "",
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

@Keep
data class ChatMessage(
    val id: String = "",
    val text: String = "",
    val isUser: Boolean = true,
    val timestamp: Long = System.currentTimeMillis(),
    val recommendedProductIds: List<String> = emptyList()
)

@Keep
data class Favorite(
    @DocumentId var id: String = "",
    val itemId: String = "",
    val itemType: String = "", // "crop", "problem", "product"
    val createdAt: Long = System.currentTimeMillis()
)

@Keep
data class MyCrop(
    @DocumentId var id: String = "",
    val cropId: String = "",
    val createdAt: Long = System.currentTimeMillis()
)

@Keep
data class Conversation(
    @DocumentId var id: String = "",
    val title: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis(),
    val messages: List<ChatMessage> = emptyList()
)

// Custom Backend API Models

@JsonClass(generateAdapter = true)
@Keep
data class ChatMessageItem(val role: String, val content: String)

@JsonClass(generateAdapter = true)
@Keep
data class AiChatRequest(
    val message: String,
    val conversationId: String = "",
    val history: List<ChatMessageItem> = emptyList()
)

@JsonClass(generateAdapter = true)
@Keep
data class AiChatResponse(
    val answer: String,
    val recommendedProducts: List<String> = emptyList()
)

@JsonClass(generateAdapter = true)
@Keep
data class ImportData(
    val crops: List<Crop> = emptyList(),
    @com.squareup.moshi.Json(name = "agricultural_problems") val agriculturalProblems: List<AgriculturalProblem> = emptyList(),
    val products: List<Product> = emptyList()
)


@JsonClass(generateAdapter = true)
@Keep
data class CartItem(
    val productId: String = "",
    val name: String = "",
    val price: Double = 0.0,
    val currency: String = "YER",
    val imageUrl: String = "",
    val quantity: Int = 1
)

@JsonClass(generateAdapter = true)
@Keep
data class Order(
    @DocumentId var id: String = "",
    val userId: String = "",
    val customerName: String = "",
    val phone: String = "",
    val governorate: String = "",
    val address: String = "",
    val items: List<CartItem> = emptyList(),
    val totalAmount: Double = 0.0,
    val currency: String = "YER",
    val paymentMethod: String = "jeeb",
    val paymentReference: String = "",
    val paymentProofUrl: String = "",
    val paymentStatus: String = "pending", // pending, submitted, approved, rejected
    val orderStatus: String = "pending", // pending, processing, approved, rejected, completed, cancelled
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)
