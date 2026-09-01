import re

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add deleteCrop after updateCrop
delete_crop_code = """    suspend fun deleteCrop(cropId: String): Result<Unit> {
        return try {
            cropsCollection.document(cropId).delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

if "fun deleteCrop" not in content:
    content = content.replace("    // --- Agricultural Problems ---", delete_crop_code + "\n\n    // --- Agricultural Problems ---")

# Add deleteProblem after updateProblem
delete_problem_code = """    suspend fun deleteProblem(problemId: String): Result<Unit> {
        return try {
            problemsCollection.document(problemId).delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }"""

if "fun deleteProblem" not in content:
    # Just append before the last closing brace
    content = re.sub(r'}\s*$', delete_problem_code + "\n}", content)

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
