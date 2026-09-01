with open("backend/src/controllers/aiController.ts", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const { message, conversationId } = req.body;", "const { message, conversationId, history } = req.body;")
content = content.replace("await aiService.processChat({ message, conversationId });", "await aiService.processChat({ message, conversationId, history });")

with open("backend/src/controllers/aiController.ts", "w", encoding="utf-8") as f:
    f.write(content)
