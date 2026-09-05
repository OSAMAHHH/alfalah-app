with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

isMyCrop_str = """    suspend fun isMyCrop(cropId: String): Boolean {
        val uid = getUserId() ?: return false
        return try {
            val doc = firestore.collection("users").document(uid).collection("my_crops").document(cropId).get().await()
            doc.exists()
        } catch (e: Exception) {
            false
        }
    }"""
    
new_str = isMyCrop_str + """

    suspend fun getMyCrops(): Result<List<String>> {
        val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("my_crops").get().await()
            val crops = snapshot.documents.map { it.id }
            Result.success(crops)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

if "getMyCrops" not in content:
    content = content.replace(isMyCrop_str, new_str)
    with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
        f.write(content)
