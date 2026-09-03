import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('delete().await()\n            Result.success(docRef.id)', 'delete().await()\n            Result.success(Unit)')

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w", encoding="utf-8") as f:
    f.write(content)
