with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()

bad = """                                else Toast.makeText(context, "حدث خطأ: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()"""

good = """                                else Toast.makeText(context, result.exceptionOrNull()?.message ?: "حدث خطأ غير معروف", Toast.LENGTH_LONG).show()"""

content = content.replace(bad, good)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)
