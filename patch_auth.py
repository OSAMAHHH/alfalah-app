import re

with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

method = """
    suspend fun resetPassword(email: String): Result<Unit> {
        return try {
            auth.sendPasswordResetEmail(email).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
"""

content = re.sub(r'}\s*$', method.strip() + '\n', content)

with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)
