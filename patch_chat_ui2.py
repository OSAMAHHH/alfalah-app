import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "r") as f:
    content = f.read()

# Remove navigationBarsPadding() since Scaffold padding already handles it
content = content.replace('.navigationBarsPadding()', '')

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "w") as f:
    f.write(content)
