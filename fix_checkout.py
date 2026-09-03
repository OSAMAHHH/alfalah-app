with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "r") as f:
    content = f.read()

content = content.replace("authRepo.getCurrentUser()", "authRepo.currentUser.value")

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("firestoreRepository.getProduct(productId)", "firestoreRepository.getProductById(productId)")

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w") as f:
    f.write(content)
