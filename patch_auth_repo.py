import re
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

functions = """
    suspend fun updateDeliveryInfo(phone: String, governorate: String, address: String): Result<Unit> {
        val uid = auth.currentUser?.uid ?: return Result.failure(Exception("Unauthorized"))
        return try {
            firestore.collection("users").document(uid).update(
                mapOf(
                    "phone" to phone,
                    "governorate" to governorate,
                    "address" to address
                )
            ).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""

content = re.sub(r'}\s*$', functions + '\n}', content)
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
