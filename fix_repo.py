import re

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    content = f.read()

# Fix getCrops
old_get_crops = """    suspend fun getCrops(): Result<List<Crop>> {
        return try {
            val snapshot = cropsCollection.get().await()
            val crops = snapshot.documents.mapNotNull { it.toObject(Crop::class.java) }
            Result.success(crops)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

new_get_crops = """    suspend fun getCrops(): Result<List<Crop>> {
        return try {
            val snapshot = cropsCollection.get().await()
            val crops = snapshot.documents.mapNotNull { doc ->
                try {
                    doc.toObject(Crop::class.java)?.let { crop ->
                        crop.copy(isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: crop.isActive)
                    }
                } catch (e: Exception) {
                    try {
                        Crop(
                            id = doc.id,
                            name = doc.getString("name") ?: "",
                            synonyms = doc.get("synonyms") as? List<String> ?: emptyList(),
                            description = doc.getString("description") ?: "",
                            plantingSeason = doc.getString("plantingSeason") ?: "",
                            soil = doc.getString("soil") ?: "",
                            irrigation = doc.getString("irrigation") ?: "",
                            fertilization = doc.getString("fertilization") ?: "",
                            notes = doc.getString("notes") ?: "",
                            isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: true
                        )
                    } catch (e2: Exception) {
                        null
                    }
                }
            }
            Result.success(crops)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

content = content.replace(old_get_crops, new_get_crops)

# Fix getProblemsForCrop
old_get_problems_crop = """    suspend fun getProblemsForCrop(cropId: String): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.whereEqualTo("cropId", cropId).get().await()
            val problems = snapshot.documents.mapNotNull { it.toObject(AgriculturalProblem::class.java) }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

new_get_problems_crop = """    suspend fun getProblemsForCrop(cropId: String): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.whereEqualTo("cropId", cropId).get().await()
            val problems = snapshot.documents.mapNotNull { doc ->
                try {
                    doc.toObject(AgriculturalProblem::class.java)?.let { problem ->
                        problem.copy(isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: problem.isActive)
                    }
                } catch (e: Exception) {
                    try {
                        AgriculturalProblem(
                            id = doc.id,
                            cropId = doc.getString("cropId") ?: "",
                            name = doc.getString("name") ?: "",
                            synonyms = doc.get("synonyms") as? List<String> ?: emptyList(),
                            type = doc.getString("type") ?: "",
                            symptoms = doc.get("symptoms") as? List<String> ?: emptyList(),
                            causes = doc.getString("causes") ?: "",
                            prevention = doc.getString("prevention") ?: "",
                            treatment = doc.getString("treatment") ?: "",
                            recommendedProductIds = doc.get("recommendedProductIds") as? List<String> ?: emptyList(),
                            isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: true
                        )
                    } catch (e2: Exception) {
                        null
                    }
                }
            }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

content = content.replace(old_get_problems_crop, new_get_problems_crop)

# Fix getProblems
old_get_problems = """    suspend fun getProblems(): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.get().await()
            val problems = snapshot.documents.mapNotNull { it.toObject(AgriculturalProblem::class.java) }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

new_get_problems = """    suspend fun getProblems(): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.get().await()
            val problems = snapshot.documents.mapNotNull { doc ->
                try {
                    doc.toObject(AgriculturalProblem::class.java)?.let { problem ->
                        problem.copy(isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: problem.isActive)
                    }
                } catch (e: Exception) {
                    try {
                        AgriculturalProblem(
                            id = doc.id,
                            cropId = doc.getString("cropId") ?: "",
                            name = doc.getString("name") ?: "",
                            synonyms = doc.get("synonyms") as? List<String> ?: emptyList(),
                            type = doc.getString("type") ?: "",
                            symptoms = doc.get("symptoms") as? List<String> ?: emptyList(),
                            causes = doc.getString("causes") ?: "",
                            prevention = doc.getString("prevention") ?: "",
                            treatment = doc.getString("treatment") ?: "",
                            recommendedProductIds = doc.get("recommendedProductIds") as? List<String> ?: emptyList(),
                            isActive = doc.getBoolean("isActive") ?: doc.getBoolean("active") ?: true
                        )
                    } catch (e2: Exception) {
                        null
                    }
                }
            }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

content = content.replace(old_get_problems, new_get_problems)

# Write back
with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(content)
