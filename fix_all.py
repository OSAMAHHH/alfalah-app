import re

# Fix AuthRepository
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()
content = content.replace("val user = result.user\n", "val user = result.user ?: throw Exception(\"User is null\")\n")
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)

# Fix AdminDashboardScreen (Argument type mismatch: actual type is 'Any', but 'String' was expected)
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()
# cropToDelete!!.id was replaced by cropToDelete ?: Crop() ? Wait.
# I had `val r = firestoreRepository.deleteCrop(cropToDelete!!.id)`
# It became `val r = firestoreRepository.deleteCrop((cropToDelete ?: Crop()).id)`
# Wait, let's fix it by regex:
content = content.replace("val r = firestoreRepository.deleteCrop((cropToDelete ?: Crop()).id)", "val r = firestoreRepository.deleteCrop(cropToDelete?.id ?: \"\")")
content = content.replace("val r = firestoreRepository.deleteProblem((problemToDelete ?: AgriculturalProblem()).id)", "val r = firestoreRepository.deleteProblem(problemToDelete?.id ?: \"\")")
# If that didn't match, let's just restore original then fix it safely.
# Actually I'll use `git checkout` for these files and fix them properly!
