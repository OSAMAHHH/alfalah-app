with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'else Toast.makeText(context, "حدث خطأ", Toast.LENGTH_SHORT).show()',
    'else Toast.makeText(context, "حدث خطأ: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace(
    'else Toast.makeText(context, "حدث خطأ", Toast.LENGTH_SHORT).show()',
    'else Toast.makeText(context, "حدث خطأ: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content2)
