with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

bad1 = 'contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}"'
good1 = 'contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\n"'
content = content.replace(bad1, good1)

bad2 = 'contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}"'
good2 = 'contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms} - العلاج: ${p.treatment}\\n"'
content = content.replace(bad2, good2)

bad3 = 'contextText += "بناءً على ذلك، أجب عن: "'
good3 = 'contextText += "\\nبناءً على ذلك، أجب عن: "'
content = content.replace(bad3, good3)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
