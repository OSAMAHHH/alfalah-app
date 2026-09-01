import re

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# I will add the missing } at the end of new_body
content = content.replace("            }\n        }\n    }\n\n@Composable\nfun CropCard", "            }\n        }\n    }\n}\n\n@Composable\nfun CropCard")

with open("app/src/main/java/com/example/alfalah/ui/screens/guide/GuideScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)

