import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "r") as f:
    text = f.read()

# Fix the string literals
text = text.replace('\\\\n', '\\n')

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatViewModel.kt", "w") as f:
    f.write(text)
