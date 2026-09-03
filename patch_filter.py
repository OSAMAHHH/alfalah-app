import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r") as f:
    content = f.read()

replacement = """
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

old_logic = """
            val matchesFilter = if (selectedFilter == "الكل") true else {
                when (item) {
                    is AgriculturalProblem -> item.type == selectedFilter
                    else -> true
                }
            }
"""

content = content.replace(old_logic.strip(), replacement.strip())

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w") as f:
    f.write(content)
