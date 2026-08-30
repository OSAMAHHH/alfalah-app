import re

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r") as f:
    text = f.read()

new_crop = """data class Crop(
    @DocumentId val id: String = "",
    val name: String = "",
    val synonyms: List<String> = emptyList(),
    val description: String = "",
    val plantingSeason: String = "",
    val soil: String = "",
    val irrigation: String = "",
    val fertilization: String = "",
    val notes: String = "",
    val isActive: Boolean = true
)"""

text = re.sub(r'data class Crop\([\s\S]*?isActive: Boolean = true\n\)', new_crop, text)

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w") as f:
    f.write(text)
