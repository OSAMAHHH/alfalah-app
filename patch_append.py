with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

new_func = """
    suspend fun getMyCrops(): List<MyCrop> {
        val uid = getUserId() ?: return emptyList()
        return try {
            val snapshot = firestore.collection("users").document(uid).collection("my_crops").get().await()
            snapshot.toObjects(MyCrop::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }
}"""

content = content.rstrip()
if content.endswith("}"):
    content = content[:-1] + new_func
    
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
