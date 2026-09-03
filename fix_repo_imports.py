with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.tasks.await", "import kotlinx.coroutines.tasks.await\nimport kotlinx.coroutines.withContext\nimport kotlinx.coroutines.Dispatchers")

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
