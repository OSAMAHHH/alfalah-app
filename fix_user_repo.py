import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Fix getConversations
get_conv = """    suspend fun getConversations(): List<Conversation> {
        val uid = getUserId() ?: return emptyList()
        return firestore.collection("users").document(uid)
            .collection("conversations")
            .orderBy("updatedAt", Query.Direction.DESCENDING)
            .get().await()
            .toObjects(Conversation::class.java)
    }"""
get_conv_new = """    suspend fun getConversations(): List<Conversation> {
        val uid = getUserId() ?: return emptyList()
        return try {
            firestore.collection("users").document(uid)
                .collection("conversations")
                .orderBy("updatedAt", Query.Direction.DESCENDING)
                .get().await()
                .toObjects(Conversation::class.java)
        } catch (e: Exception) {
            emptyList()
        }
    }"""
content = content.replace(get_conv, get_conv_new)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
