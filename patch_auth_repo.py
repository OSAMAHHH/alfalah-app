with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

update_func = """
    suspend fun updateUserName(newName: String): Result<Unit> {
        val user = auth.currentUser ?: return Result.failure(Exception("غير مسجل الدخول"))
        return try {
            firestore.collection("users").document(user.uid)
                .update("name", newName).await()
            
            // Update local state directly to reflect immediately
            _currentUser.value = _currentUser.value?.copy(name = newName)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun logout() {"""

content = content.replace("    fun logout() {", update_func)

with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
