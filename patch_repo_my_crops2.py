with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

bad_func = """    suspend fun getMyCrops(): Result<List<String>> {
        val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("my_crops").get().await()
            val crops = snapshot.documents.map { it.id }
            Result.success(crops)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""
    
good_func = """    suspend fun getMyCrops(): List<MyCrop> {
        val uid = getUserId() ?: return emptyList()
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("my_crops").get().await()
            snapshot.toObjects(MyCrop::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }"""

content = content.replace(bad_func, good_func)
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
