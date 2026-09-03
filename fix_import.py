with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "r") as f:
    content = f.read()

content = content.replace("context.contentResolver.openInputStream(selectedUri)", "context.contentResolver.openInputStream(selectedUri ?: throw Exception(\"URI is null\"))")
content = content.replace("val crops = parsedJson.getJSONArray(\"crops\")", "val crops = (parsedJson ?: throw Exception(\"JSON is null\")).getJSONArray(\"crops\")")
content = content.replace("val problems = parsedJson.getJSONArray(\"agricultural_problems\")", "val problems = (parsedJson ?: throw Exception(\"JSON is null\")).getJSONArray(\"agricultural_problems\")")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "w") as f:
    f.write(content)
