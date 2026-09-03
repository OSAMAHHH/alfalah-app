import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

# Add Cart and Orders functions before the last brace
functions = """
    // --- Cart ---
    suspend fun getCartItems(): Result<List<com.example.alfalah.data.model.CartItem>> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("cart").get().await()
            val items = snapshot.documents.mapNotNull { it.toObject(com.example.alfalah.data.model.CartItem::class.java) }
            Result.success(items)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addToCart(item: com.example.alfalah.data.model.CartItem): Result<Unit> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val docRef = firestore.collection("users").document(uid).collection("cart").document(item.productId)
            val snapshot = docRef.get().await()
            if (snapshot.exists()) {
                val existing = snapshot.toObject(com.example.alfalah.data.model.CartItem::class.java)
                if (existing != null) {
                    docRef.update("quantity", existing.quantity + 1).await()
                }
            } else {
                docRef.set(item).await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateCartQuantity(productId: String, quantity: Int): Result<Unit> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val docRef = firestore.collection("users").document(uid).collection("cart").document(productId)
            if (quantity <= 0) {
                docRef.delete().await()
            } else {
                docRef.update("quantity", quantity).await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun clearCart(): Result<Unit> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("cart").get().await()
            val batch = firestore.batch()
            for (doc in snapshot.documents) {
                batch.delete(doc.reference)
            }
            batch.commit().await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // --- Orders ---
    suspend fun createOrder(order: com.example.alfalah.data.model.Order): Result<String> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val docRef = firestore.collection("orders").document()
            val finalOrder = order.copy(id = docRef.id, userId = uid)
            docRef.set(finalOrder).await()
            Result.success(docRef.id)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getMyOrders(): Result<List<com.example.alfalah.data.model.Order>> {
        val uid = getUserId() ?: return Result.failure(Exception("Unauthorized"))
        return try {
            val snapshot = firestore.collection("orders")
                .whereEqualTo("userId", uid)
                .get().await()
            val orders = snapshot.documents.mapNotNull { it.toObject(com.example.alfalah.data.model.Order::class.java) }
                .sortedByDescending { it.createdAt }
            Result.success(orders)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getAllOrders(): Result<List<com.example.alfalah.data.model.Order>> {
        return try {
            val snapshot = firestore.collection("orders")
                .get().await()
            val orders = snapshot.documents.mapNotNull { it.toObject(com.example.alfalah.data.model.Order::class.java) }
                .sortedByDescending { it.createdAt }
            Result.success(orders)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateOrderStatus(orderId: String, paymentStatus: String, orderStatus: String): Result<Unit> {
        return try {
            firestore.collection("orders").document(orderId)
                .update(
                    mapOf(
                        "paymentStatus" to paymentStatus,
                        "orderStatus" to orderStatus,
                        "updatedAt" to System.currentTimeMillis()
                    )
                ).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""

content = re.sub(r'}\s*$', functions + '\n}', content)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
