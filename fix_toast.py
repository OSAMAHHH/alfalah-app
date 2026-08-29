import re
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

text = re.sub(r'if \(isAdding\) firestoreRepository\.addCrop\(c\) else firestoreRepository\.updateCrop\(c\)', 'val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)\n                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()', text)
text = re.sub(r'if \(isAdding\) firestoreRepository\.addProblem\(pr\) else firestoreRepository\.updateProblem\(pr\)', 'val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)\n                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()', text)
text = re.sub(r'if \(isAdding\) firestoreRepository\.addProduct\(p\) else firestoreRepository\.updateProduct\(p\)', 'val r = if (isAdding) firestoreRepository.addProduct(p) else firestoreRepository.updateProduct(p)\n                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()', text)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
