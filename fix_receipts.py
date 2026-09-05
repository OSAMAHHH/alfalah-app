with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()
content = content.replace('.child("receipts/$uid/', '.child("payment_receipts/$uid/')
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
