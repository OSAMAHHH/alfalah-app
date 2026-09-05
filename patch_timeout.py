import re

with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "r") as f:
    content = f.read()

content = content.replace('.connectTimeout(30, TimeUnit.SECONDS)', '.connectTimeout(60, TimeUnit.SECONDS)')
content = content.replace('.readTimeout(30, TimeUnit.SECONDS)', '.readTimeout(60, TimeUnit.SECONDS)')
content = content.replace('.writeTimeout(30, TimeUnit.SECONDS)', '.writeTimeout(60, TimeUnit.SECONDS)') # if exists

with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "w") as f:
    f.write(content)
