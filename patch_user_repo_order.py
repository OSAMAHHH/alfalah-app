with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

old_fn = """    suspend fun updateOrderStatus(orderId: String, status: String): Result<Unit> {
        return try {
            firestore.collection("orders").document(orderId)
                .update("orderStatus", status, "updatedAt", System.currentTimeMillis()).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

new_fn = """    suspend fun updateOrderStatus(orderId: String, paymentStatus: String, orderStatus: String): Result<Unit> {
        return try {
            firestore.collection("orders").document(orderId)
                .update("paymentStatus", paymentStatus, "orderStatus", orderStatus, "updatedAt", System.currentTimeMillis()).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

content = content.replace(old_fn, new_fn)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
