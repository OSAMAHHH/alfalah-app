import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "r") as f:
    content = f.read()

validation_code = """
                                        if (problem.has("recommendedProductIds")) {
                                            val pIds = problem.getJSONArray("recommendedProductIds")
                                            if (pIds.length() > 0) {
                                                errors.add("الملف يحتوي recommendedProductIds وهذا غير مدعوم في الفحص الحالي (الدفعة الأولى لا تحتوي منتجات)")
                                                hasErrors = true
                                            }
                                        }
"""
content = re.sub(r'if \(problem\.has\("type"\)\) \{', validation_code.strip() + '\n                                        if (problem.has("type")) {', content, flags=re.DOTALL)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/ImportDatabaseScreen.kt", "w") as f:
    f.write(content)
