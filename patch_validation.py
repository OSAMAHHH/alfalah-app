import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "r") as f:
    content = f.read()

validation_code = """
                                        if (!problem.has("cropId")) {
                                            errors.add("مشكلة بدون cropId")
                                            hasErrors = true
                                        } else {
                                            val cId = problem.getString("cropId")
                                            if (!cropIds.contains(cId)) {
                                                errors.add("مشكلة تشير لمحصول غير موجود بالملف: $cId")
                                                hasErrors = true
                                            }
                                        }
"""
content = re.sub(r'if \(!problem\.has\("cropId"\)\) \{.*?// We\'ll just assume they must exist in the JSON or DB\. For batch 1 they are in JSON\.\s*\}', validation_code.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "w") as f:
    f.write(content)
