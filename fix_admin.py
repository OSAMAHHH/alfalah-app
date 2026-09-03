with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

content = content.replace("firestoreRepository.deleteCrop((cropToDelete ?: Crop()).id)", "firestoreRepository.deleteCrop(cropToDelete?.id ?: \"\")")
content = content.replace("firestoreRepository.deleteProblem((problemToDelete ?: AgriculturalProblem()).id)", "firestoreRepository.deleteProblem(problemToDelete?.id ?: \"\")")

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)
