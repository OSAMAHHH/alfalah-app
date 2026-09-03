import sys

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    content = f.read()

content = content.replace("suspend fun getCropsPaginated(lastDoc: DocumentSnapshot? = null)", "suspend fun getCropsPaginated(limit: Int, lastDoc: DocumentSnapshot? = null)")
content = content.replace("firestore.collection(\"crops\").limit(20)", "firestore.collection(\"crops\").limit(limit.toLong())")

content = content.replace("suspend fun getProblemsPaginated(lastDoc: DocumentSnapshot? = null)", "suspend fun getProblemsPaginated(limit: Int, lastDoc: DocumentSnapshot? = null)")
content = content.replace("firestore.collection(\"problems\").limit(20)", "firestore.collection(\"problems\").limit(limit.toLong())")

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(content)
