import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

get_fav = """    suspend fun getFavorites(): List<Favorite> {
        val uid = getUserId() ?: return emptyList()
        return firestore.collection("users").document(uid)
            .collection("favorites")
            .orderBy("createdAt", Query.Direction.DESCENDING)
            .get().await()
            .toObjects(Favorite::class.java)
    }"""
get_fav_new = """    suspend fun getFavorites(): List<Favorite> {
        val uid = getUserId() ?: return emptyList()
        return try {
            firestore.collection("users").document(uid)
                .collection("favorites")
                .orderBy("createdAt", Query.Direction.DESCENDING)
                .get().await()
                .toObjects(Favorite::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }"""
content = content.replace(get_fav, get_fav_new)

get_my_crops = """    suspend fun getMyCrops(): Result<List<MyCrop>> {
        val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))
        return try {
            val snapshot = firestore.collection("users").document(uid)
                .collection("my_crops")
                .orderBy("createdAt", Query.Direction.DESCENDING)
                .get().await()
            Result.success(snapshot.toObjects(MyCrop::class.java))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""
# Already wrapped in try-catch in getMyCrops. 

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
