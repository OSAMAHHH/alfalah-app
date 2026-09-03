import re
with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r") as f:
    content = f.read()

old_logic = """
            val matchesFilter = if (selectedFilter == "الكل") true else {
                val englishFilter = when (selectedFilter) {
                    "الأمراض" -> "disease"
                    "الآفات" -> "pest"
                    "نقص العناصر الغذائية" -> "deficiency"
                    "مشاكل أخرى" -> "other"
                    else -> selectedFilter
                }
                when (item) {
                    is AgriculturalProblem -> item.type == englishFilter
                    else -> true
                }
            }
"""

new_logic = """
            val matchesFilter = if (selectedFilter == "الكل") true else {
                val englishFilter = when (selectedFilter) {
                    "الأمراض" -> listOf("disease", "أمراض", "مرض")
                    "الآفات" -> listOf("pest", "آفات", "آفة")
                    "نقص العناصر الغذائية" -> listOf("deficiency", "nutrient_deficiency", "نقص")
                    "مشاكل أخرى" -> listOf("other", "irrigation_problem", "soil_problem", "أخرى")
                    else -> listOf(selectedFilter)
                }
                when (item) {
                    is AgriculturalProblem -> englishFilter.any { item.type.equals(it, ignoreCase = true) } || englishFilter.any { item.type.contains(it, ignoreCase = true) }
                    else -> true
                }
            }
"""

content = content.replace(old_logic.strip(), new_logic.strip())

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w") as f:
    f.write(content)
