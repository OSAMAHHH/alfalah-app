import re

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    text = f.read()

import_lines = "import kotlinx.coroutines.Dispatchers\nimport kotlinx.coroutines.withContext\n"
text = text.replace("import kotlinx.coroutines.tasks.await", "import kotlinx.coroutines.tasks.await\n" + import_lines)

upload_func = """
    suspend fun uploadImage(uri: Uri): Result<String> = withContext(Dispatchers.IO) {
        try {
            val storageRef = FirebaseStorage.getInstance().reference.child("products/${UUID.randomUUID()}.jpg")
            storageRef.putFile(uri).await()
            val downloadUrl = storageRef.downloadUrl.await().toString()
            Result.success(downloadUrl)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""

text = text.replace("suspend fun getProducts():", upload_func + "\n    suspend fun getProducts():")

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(text)
