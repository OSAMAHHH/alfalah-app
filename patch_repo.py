with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

addToCart_str = """    suspend fun addToCart(item: CartItem): Result<Unit> {
        val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))
        return try {
            firestore.collection("users").document(uid)
                .collection("cart").document(item.productId)
                .set(item).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""
    
new_str = addToCart_str + """

    suspend fun updateCartQuantity(productId: String, quantity: Int): Result<Unit> {
        val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))
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
    }"""

content = content.replace(addToCart_str, new_str)
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
