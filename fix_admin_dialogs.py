import re
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

text = re.sub(r'val r = if \(isAdding\) firestoreRepository\.addCrop\(c\) else firestoreRepository\.updateCrop\(c\)\s*if \(r\.isFailure\) Toast\.makeText\(context, r\.exceptionOrNull\(\)\?\.message \?\: "Error", Toast\.LENGTH_SHORT\)\.show\(\)', 'if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)', text)
text = re.sub(r'val r = if \(isAdding\) firestoreRepository\.addProblem\(pr\) else firestoreRepository\.updateProblem\(pr\)\s*if \(r\.isFailure\) Toast\.makeText\(context, r\.exceptionOrNull\(\)\?\.message \?\: "Error", Toast\.LENGTH_SHORT\)\.show\(\)', 'if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)', text)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
