with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r") as f:
    content = f.read()

content = content.replace('@DocumentId val id: String = ""', '@DocumentId var id: String = ""')

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w") as f:
    f.write(content)
