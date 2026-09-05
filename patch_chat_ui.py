import re

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "r") as f:
    content = f.read()

# Fix layout: add imePadding
content = content.replace(
    'Column(modifier = modifier.fillMaxSize().padding(padding)) {',
    'Column(modifier = modifier.fillMaxSize().padding(padding).imePadding()) {'
)

# And remove navigationBarsPadding() from the Row to avoid double padding if imePadding covers it?
# Actually, imePadding() is additive. If keyboard is closed, ime is 0, so we need navigationBarsPadding.
# But wait, we should just use WindowInsets on the Scaffold if possible. 
# In Compose, Scaffold padding includes the system bars if you don't specify contentWindowInsets.
# The BottomAppBar or bottom row should sit above the nav bar.
# The original code has: `Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp).navigationBarsPadding()`
# This is fine. By adding `.imePadding()` to the `Column`, the whole column gets pushed up by the keyboard.

with open("app/src/main/java/com/example/alfalah/ui/screens/chat/ChatScreen.kt", "w") as f:
    f.write(content)
