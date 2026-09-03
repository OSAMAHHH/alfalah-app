import re

def fix_screen(file_path, var_name):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # We will replace all occurrences of `var_name!!` with `p` where we define `val p = var_name`
    # or just `p.`
    
    # Actually, simpler: replace var_name!!.prop with var_name?.prop ?: ""
    # Or just replace `var_name!!` with `var_name?` where safe, or `(var_name ?: return@Column)`
    # But for compose, we can just find where the content is rendered and use a local val.
    
    # A generic fix: replace `var_name!!` with `var_name?` and use `?: ""` for strings.
    # But there's a better way: let's replace all `var_name!!` with `it` and wrap the block in `var_name?.let { it ->`
    pass

# For ProductDetailsScreen:
with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("product!!", "p")
# We need to inject `val p = product; if (p != null) {` where appropriate.
# Let's just do simple regex replacement:
content = re.sub(r'Text\(p\.([a-zA-Z0-9_]+)', r'Text(product?.\1 ?: ""', content)
content = re.sub(r'p\.([a-zA-Z0-9_]+)\.isNotBlank', r'(product?.\1?.isNotBlank() == true)', content)
content = re.sub(r'p\.([a-zA-Z0-9_]+)\.ifEmpty', r'(product?.\1 ?: "").ifEmpty', content)
content = re.sub(r'p\.([a-zA-Z0-9_]+)', r'product?.\1 ?: ""', content) # fallback for others

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content)

# For CropDetailsScreen:
with open("app/src/main/java/com/example/alfalah/ui/screens/guide/CropDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("crop!!", "c")
content = re.sub(r'Text\(c\.([a-zA-Z0-9_]+)', r'Text(crop?.\1 ?: ""', content)
content = re.sub(r'c\.([a-zA-Z0-9_]+)\.isNotEmpty', r'(crop?.\1?.isNotEmpty() == true)', content)
content = re.sub(r'c\.([a-zA-Z0-9_]+)', r'crop?.\1 ?: ""', content)

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/CropDetailsScreen.kt", "w") as f:
    f.write(content)

# For ProblemDetailsScreen:
with open("app/src/main/java/com/example/alfalah/ui/screens/guide/ProblemDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("problem!!", "pr")
content = re.sub(r'pr\.([a-zA-Z0-9_]+)\.isNotEmpty', r'(problem?.\1?.isNotEmpty() == true)', content)
content = re.sub(r'pr\.([a-zA-Z0-9_]+)\.joinToString', r'(problem?.\1?.joinToString ?: "")', content)
content = re.sub(r'pr\.([a-zA-Z0-9_]+)', r'problem?.\1 ?: ""', content)
content = content.replace('relatedCrop!!', 'relatedCrop?')

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/ProblemDetailsScreen.kt", "w") as f:
    f.write(content)

# For ProfileScreen:
with open("app/src/main/java/com/example/alfalah/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()
content = content.replace("currentUser!!.name", "currentUser?.name ?: \"\"")
with open("app/src/main/java/com/example/alfalah/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
    
# For AdminDashboardScreen:
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()
content = content.replace("showProductDialog!!", "showProductDialog ?: Product()")
content = content.replace("showCropDialog!!", "showCropDialog ?: Crop()")
content = content.replace("showProblemDialog!!", "showProblemDialog ?: AgriculturalProblem()")
content = content.replace("cropToDelete!!", "cropToDelete ?: Crop()")
content = content.replace("problemToDelete!!", "problemToDelete ?: AgriculturalProblem()")
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)

# AuthRepository:
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()
content = content.replace("result.user!!.uid", "result.user?.uid ?: \"\"")
content = content.replace("result.user!!", "result.user")
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)

# ChatViewModel
with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()
content = content.replace("currentConversation!!.messages", "currentConversation?.messages ?: emptyList()")
content = content.replace("currentConversation!!.title", "currentConversation?.title ?: \"\"")
with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
    
# ImportDatabaseScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "r") as f:
    content = f.read()
content = content.replace("selectedUri!!", "selectedUri")
content = content.replace("parsedJson!!", "parsedJson")
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "w") as f:
    f.write(content)
    
# StoreScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()
content = content.replace("errorMsg!!", "errorMsg ?: \"\"")
with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)

