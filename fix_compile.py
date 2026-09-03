import re

# Fix ProblemDetailsScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/guide/ProblemDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace('(problem?.symptoms?.isNotEmpty() == true)()', '(problem?.symptoms?.isNotEmpty() == true)')
content = content.replace('(problem?.symptoms?.joinToString ?: "")("، ")', 'problem?.symptoms?.joinToString("، ") ?: ""')
content = content.replace('relatedCrop?.name', 'relatedCrop?.name ?: ""')

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/ProblemDetailsScreen.kt", "w") as f:
    f.write(content)

# Fix CropDetailsScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/guide/CropDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace('(crop?.description?.isNotEmpty() == true)()', '(crop?.description?.isNotEmpty() == true)')
content = content.replace('(crop?.plantingSeason?.isNotEmpty() == true)()', '(crop?.plantingSeason?.isNotEmpty() == true)')
content = content.replace('(crop?.soil?.isNotEmpty() == true)()', '(crop?.soil?.isNotEmpty() == true)')
content = content.replace('(crop?.irrigation?.isNotEmpty() == true)()', '(crop?.irrigation?.isNotEmpty() == true)')
content = content.replace('(crop?.fertilization?.isNotEmpty() == true)()', '(crop?.fertilization?.isNotEmpty() == true)')
content = content.replace('(crop?.notes?.isNotEmpty() == true)()', '(crop?.notes?.isNotEmpty() == true)')

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/CropDetailsScreen.kt", "w") as f:
    f.write(content)

# Fix ProductDetailsScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace('(product?.usage?.isNotBlank() == true)()', '(product?.usage?.isNotBlank() == true)')
content = content.replace('(product?.dosage?.isNotBlank() == true)()', '(product?.dosage?.isNotBlank() == true)')
content = content.replace('(product?.warnings?.isNotBlank() == true)()', '(product?.warnings?.isNotBlank() == true)')

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content)

