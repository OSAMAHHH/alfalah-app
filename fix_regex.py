import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

content = re.sub(r'contextText \+= "المحصول: .*?"', 'contextText += "المحصول: ${c.name} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\\\n"', content)
content = re.sub(r'contextText \+= "المشكلة: .*?"', 'contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms} - العلاج: ${p.treatment}\\\\n"', content)
content = re.sub(r'contextText \+= "بناءً على ذلك، أجب عن: "', 'contextText += "\\\\nبناءً على ذلك، أجب عن: "', content)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
