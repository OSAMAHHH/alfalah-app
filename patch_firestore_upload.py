with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    content = f.read()

import_str = "import com.google.firebase.firestore.FirebaseFirestore"
import_str_new = "import com.google.firebase.firestore.FirebaseFirestore\nimport com.google.firebase.storage.FirebaseStorage\nimport android.net.Uri\nimport java.util.UUID"

upload_fn = """
    suspend fun uploadImage(uri: Uri): Result<String> = try {
        val storage = FirebaseStorage.getInstance()
        val ref = storage.reference.child("images/${UUID.randomUUID()}")
        ref.putFile(uri).await()
        Result.success(ref.downloadUrl.await().toString())
    } catch (e: Exception) { Result.failure(e) }
}"""

content = content.replace(import_str, import_str_new)
content = content.replace("}\n", upload_fn + "\n")

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(content)
