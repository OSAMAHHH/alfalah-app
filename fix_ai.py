import re

with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "r") as f:
    content = f.read()

# Add FirestoreRepository instance
if "private val firestoreRepo" not in content:
    content = content.replace("class AiRepository {", "class AiRepository {\n    private val firestoreRepo = FirestoreRepository()\n")

# Inject knowledge base logic before calling API
logic = """
            // ---- Local Knowledge Base Search ----
            val lowerMsg = message.lowercase()
            val crops = firestoreRepo.getCrops().getOrNull() ?: emptyList()
            val problems = firestoreRepo.getProblems().getOrNull() ?: emptyList()
            
            val matchedProblem = problems.find { p ->
                lowerMsg.contains(p.name.lowercase()) || p.synonyms.any { lowerMsg.contains(it.lowercase()) }
            }
            if (matchedProblem != null) {
                val ans = "بناءً على قاعدة المعرفة المحلية:\\nالمشكلة: ${matchedProblem.name}\\nالأعراض: ${matchedProblem.symptoms.joinToString("، ")}\\nالعلاج: ${matchedProblem.treatment}"
                return@withContext Pair(ans, matchedProblem.recommendedProductIds)
            }
            
            val matchedCrop = crops.find { c ->
                lowerMsg.contains(c.name.lowercase()) || c.synonyms.any { lowerMsg.contains(it.lowercase()) }
            }
            if (matchedCrop != null) {
                val ans = "بناءً على قاعدة المعرفة المحلية:\\nالمحصول: ${matchedCrop.name}\\nالوصف: ${matchedCrop.description}\\nموسم الزراعة: ${matchedCrop.plantingSeason}\\nطرق الري: ${matchedCrop.irrigation}\\nالتسميد: ${matchedCrop.fertilization}"
                return@withContext Pair(ans, emptyList())
            }
            // ---- End Local Search ----

"""

content = content.replace("val token = \"Bearer ${tokenResult.token}\"", "val token = \"Bearer ${tokenResult.token}\"\n" + logic)

with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "w") as f:
    f.write(content)
