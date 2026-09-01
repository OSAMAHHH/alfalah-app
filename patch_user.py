with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r", encoding="utf-8") as f:
    content = f.read()

old_user = """data class User(
    @DocumentId val id: String = "",
    val name: String = "",
    val email: String = "",
    val role: String = "user" // "user" or "admin"
)"""

new_user = """data class User(
    @DocumentId val id: String = "",
    val name: String = "",
    val email: String = "",
    val role: String = "user", // "user" or "admin"
    val photoUrl: String? = null
)"""

content = content.replace(old_user, new_user)

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w", encoding="utf-8") as f:
    f.write(content)
