import re
with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r") as f:
    content = f.read()

content = content.replace("import com.squareup.moshi.JsonClass", "import com.squareup.moshi.JsonClass\nimport androidx.annotation.Keep")
content = re.sub(r"data class ", "@Keep\ndata class ", content)

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w") as f:
    f.write(content)
