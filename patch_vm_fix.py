import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    content = f.read()

# Replace the problematic line
bad_line = 'contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms.joinToString("، ")} - العلاج: ${p.treatment.joinToString("، ")}"'
good_line = 'contextText += "المشكلة: ${p.name} - الأعراض: ${p.symptoms} - العلاج: ${p.treatment}\\n"'

content = content.replace(bad_line, good_line)

# Also fix the crops line just in case
bad_crop_line = 'contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}"'
good_crop_line = 'contextText += "المحصول: ${c.name} - الوصف: ${c.description} - الزراعة: ${c.plantingSeason} - الري: ${c.wateringSchedule}\\n"'

content = content.replace(bad_crop_line, good_crop_line)

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(content)
