with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()
content = content.replace('.collection("my_crops")', '.collection("myCrops")')
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "r") as f:
    content = f.read()
content = content.replace('.collection("problems")', '.collection("agricultural_problems")')
content = content.replace('child("images/${UUID.randomUUID()}")', 'child("products/${UUID.randomUUID()}")')
with open("app/src/main/java/com/example/alfalah/data/repository/FirestoreRepository.kt", "w") as f:
    f.write(content)
