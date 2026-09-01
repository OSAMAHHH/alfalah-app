import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace addCrop/updateCrop toasts
old_crop_save = """val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        showCropDialog = null"""

new_crop_save = """val r = if (isAdding) firestoreRepository.addCrop(c) else firestoreRepository.updateCrop(c)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المحصول بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showCropDialog = null"""

content = content.replace(old_crop_save, new_crop_save)

# Replace addProblem/updateProblem toasts
old_problem_save = """val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        showProblemDialog = null"""

new_problem_save = """val r = if (isAdding) firestoreRepository.addProblem(pr) else firestoreRepository.updateProblem(pr)
                        if (r.isFailure) android.widget.Toast.makeText(context, r.exceptionOrNull()?.message ?: "Error", android.widget.Toast.LENGTH_LONG).show()
                        else android.widget.Toast.makeText(context, "تم حفظ المشكلة بنجاح", android.widget.Toast.LENGTH_SHORT).show()
                        showProblemDialog = null"""

content = content.replace(old_problem_save, new_problem_save)


with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

