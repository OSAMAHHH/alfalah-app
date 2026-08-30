import re

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    text = f.read()

import_lines = """import com.google.firebase.storage.FirebaseStorage
import android.net.Uri
import java.util.UUID"""

text = text.replace("import com.google.firebase.firestore.FirebaseFirestore", "import com.google.firebase.firestore.FirebaseFirestore\n" + import_lines)

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

text = text.replace("    // Products", upload_func + "\n    // Products")

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(text)
