import re

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the duplicated block I added at the top
duplicate_block = """    suspend fun getProblemsForCrop(cropId: String): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = firestore.collection("agricultural_problems")
                .whereEqualTo("cropId", cropId)
                .whereEqualTo("isActive", true)
                .get().await()
            Result.success(snapshot.toObjects(AgriculturalProblem::class.java))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

content = content.replace(duplicate_block, "")

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
