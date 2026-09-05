with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

new_content = content.replace(
'''    suspend fun addToCart(item: CartItem): Result<Unit> {
        val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }
        return try {
            firestore.collection("users").document(uid)
                .collection("cart").document(item.productId)
                .set(item).await()
            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }
    }''',
'''    suspend fun addToCart(item: CartItem): Result<Unit> {
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
    }'''
)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(new_content)
