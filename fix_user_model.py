import re
with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val photoUrl: String? = null\n)',
    'val photoUrl: String? = null,\n    val phone: String = "",\n    val governorate: String = "",\n    val address: String = ""\n)'
)

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w") as f:
    f.write(content)
