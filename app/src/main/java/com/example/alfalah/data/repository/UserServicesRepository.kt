package com.example.alfalah.data.repository

import android.net.Uri
import com.example.alfalah.data.model.*
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await
import java.util.UUID

class UserServicesRepository {
    private val firestore = FirebaseFirestore.getInstance()
    private val auth = FirebaseAuth.getInstance()
    private val storage = FirebaseStorage.getInstance()

    private fun getUserId(): String? = auth.currentUser?.uid

    suspend fun getConversations(): List<Conversation> {
        val uid = getUserId() ?: return emptyList()
        return try {
            firestore.collection("users").document(uid)
                .collection("conversations")
                .orderBy("updatedAt", Query.Direction.DESCENDING)
                .get().await()
                .toObjects(Conversation::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }

    suspend fun getMyOrders(): Result<List<Order>> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val snapshot = firestore.collection("orders")
                .whereEqualTo("userId", uid)
                .get().await()
            val orders = snapshot.toObjects(Order::class.java).sortedByDescending { it.createdAt }
            Result.success(orders)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getCartItems(): Result<List<CartItem>> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val snapshot = firestore.collection("users").document(uid)
                .collection("cart")
                .get().await()
            Result.success(snapshot.toObjects(CartItem::class.java))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addToCart(item: CartItem): Result<Unit> {
        val uid = getUserId() ?: run { 
            android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in")
            return Result.failure(Exception("عليك تسجيل الدخول أولاً")) 
        }
        if (item.productId.isEmpty()) {
            return Result.failure(Exception("معرف المنتج غير صالح (فارغ)"))
        }
        return try {
            firestore.collection("users").document(uid)
                .collection("cart").document(item.productId)
                .set(item).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun updateCartQuantity(productId: String, quantity: Int): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val docRef = firestore.collection("users").document(uid).collection("cart").document(productId)
            if (quantity <= 0) {
                docRef.delete().await()
            } else {
                docRef.update("quantity", quantity).await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun clearCart(): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val snapshot = firestore.collection("users").document(uid)
                .collection("cart").get().await()
            for (doc in snapshot.documents) {
                doc.reference.delete().await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun createOrder(order: Order): Result<Boolean> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            firestore.collection("orders").add(order.copy(userId = uid)).await()
            Result.success(true)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun uploadPaymentReceipt(uri: Uri): Result<String> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val ref = storage.reference.child("payment_receipts/$uid/${UUID.randomUUID()}")
            ref.putFile(uri).await()
            val url = ref.downloadUrl.await().toString()
            Result.success(url)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getFavorites(): List<Favorite> {
        val uid = getUserId() ?: return emptyList()
        return try {
            firestore.collection("users").document(uid)
                .collection("favorites")
                .get().await()
                .toObjects(Favorite::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }

    suspend fun addFavorite(itemId: String, itemType: String): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val fav = Favorite(id = itemId, itemId = itemId, itemType = itemType)
            firestore.collection("users").document(uid)
                .collection("favorites").document(itemId)
                .set(fav).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun removeFavorite(itemId: String): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            firestore.collection("users").document(uid)
                .collection("favorites").document(itemId)
                .delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun uploadImage(uri: Uri): Result<String> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val ref = storage.reference.child("images/${UUID.randomUUID()}")
            ref.putFile(uri).await()
            val url = ref.downloadUrl.await().toString()
            Result.success(url)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getAllOrders(): Result<List<Order>> {
        return try {
            val snapshot = firestore.collection("orders")
                .get().await()
            val orders = snapshot.toObjects(Order::class.java).sortedByDescending { it.createdAt }
            Result.success(orders)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateOrderStatus(orderId: String, paymentStatus: String, orderStatus: String): Result<Unit> {
        return try {
            firestore.collection("orders").document(orderId)
                .update("paymentStatus", paymentStatus, "orderStatus", orderStatus, "updatedAt", System.currentTimeMillis()).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun isFavorite(itemId: String): Boolean {
        val uid = getUserId() ?: return false
        return try {
            val doc = firestore.collection("users").document(uid)
                .collection("favorites").document(itemId).get().await()
            doc.exists()
        } catch (e: Exception) {
            false
        }
    }

    suspend fun isMyCrop(cropId: String): Boolean {
        val uid = getUserId() ?: return false
        return try {
            val doc = firestore.collection("users").document(uid)
                .collection("myCrops").document(cropId).get().await()
            doc.exists()
        } catch (e: Exception) {
            false
        }
    }

    suspend fun addMyCrop(cropId: String): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val mc = MyCrop(id = cropId, cropId = cropId)
            firestore.collection("users").document(uid)
                .collection("myCrops").document(cropId).set(mc).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun removeMyCrop(cropId: String): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            firestore.collection("users").document(uid)
                .collection("myCrops").document(cropId).delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun deleteConversation(id: String): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            firestore.collection("users").document(uid)
                .collection("conversations").document(id).delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun saveConversation(conv: Conversation): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            val ref = if (conv.id.isEmpty()) {
                firestore.collection("users").document(uid).collection("conversations").document()
            } else {
                firestore.collection("users").document(uid).collection("conversations").document(conv.id)
            }
            ref.set(conv.copy(id = ref.id)).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }

    suspend fun getMyCrops(): List<MyCrop> {
        val uid = getUserId() ?: return emptyList()
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("myCrops").get().await()
            snapshot.toObjects(MyCrop::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }
}