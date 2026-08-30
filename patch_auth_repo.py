import re

with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    text = f.read()

import_google_auth = """import com.google.firebase.auth.GoogleAuthProvider
"""
text = text.replace("import com.google.firebase.auth.FirebaseAuth", import_google_auth + "import com.google.firebase.auth.FirebaseAuth")

google_signin_func = """
    suspend fun googleSignIn(idToken: String): Result<Unit> {
        return try {
            val credential = GoogleAuthProvider.getCredential(idToken, null)
            val result = auth.signInWithCredential(credential).await()
            val user = result.user!!
            // Check if user exists in Firestore
            val doc = firestore.collection("users").document(user.uid).get().await()
            if (!doc.exists()) {
                val newUser = User(id = user.uid, name = user.displayName ?: "مزارع", email = user.email ?: "", role = "user")
                firestore.collection("users").document(user.uid).set(newUser).await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""
text = text.replace("fun logout() {", google_signin_func + "\n    fun logout() {")

with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w") as f:
    f.write(text)
