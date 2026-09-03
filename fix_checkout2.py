with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "r") as f:
    content = f.read()

replacement = """
            val user = authRepo.currentUser.value
            if (user != null) {
                name = user.name
                phone = user.phone
                governorate = user.governorate
                address = user.address
            }
"""

content = content.replace(
    'val user = authRepo.currentUser.value\n            if (user != null) {\n                name = user.name\n                // For demonstration, these fields might be empty if we haven\'t fetched them from Firestore\n                // We would fetch the full user doc here to get phone, gov, address, but for simplicity let\'s allow input if missing.\n            }',
    replacement
)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "w") as f:
    f.write(content)
