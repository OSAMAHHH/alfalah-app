import re

# 1. Update UserServicesRepository
with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

upload_func = """    suspend fun uploadPaymentReceipt(uri: android.net.Uri): Result<String> = withContext(kotlinx.coroutines.Dispatchers.IO) {
        val uid = getUserId() ?: return@withContext Result.failure(Exception("Unauthorized"))
        try {
            val storageRef = com.google.firebase.storage.FirebaseStorage.getInstance().reference.child("payment_receipts/$uid/${java.util.UUID.randomUUID()}.jpg")
            storageRef.putFile(uri).await()
            val downloadUrl = storageRef.downloadUrl.await().toString()
            Result.success(downloadUrl)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createOrder(order: com.example.alfalah.data.model.Order): Result<String> {"""

content = content.replace('    suspend fun createOrder(order: com.example.alfalah.data.model.Order): Result<String> {', upload_func)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)


# 2. Update CheckoutScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "r") as f:
    content = f.read()

content = content.replace("val uploadResult = firestoreRepo.uploadImage(paymentProofUri!!)", "val uploadResult = userRepo.uploadPaymentReceipt(paymentProofUri!!)")

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "w") as f:
    f.write(content)

# 3. Update AdminDashboardScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    content = f.read()

new_when = """                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false }, { c -> cropToDelete = c })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false }, { pr -> problemToDelete = pr })
                    3 -> AdminOrdersScreen()
                }"""

content = content.replace("""                when (selectedTab) {
                    0 -> ProductsList(products, { p -> showProductDialog = p; isAdding = false }, { p -> scope.launch { firestoreRepository.deleteProduct(p.id); loadData() } })
                    1 -> CropsList(crops, { c -> showCropDialog = c; isAdding = false }, { c -> cropToDelete = c })
                    2 -> ProblemsList(problems, crops, { pr -> showProblemDialog = pr; isAdding = false }, { pr -> problemToDelete = pr })
                }""", new_when)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(content)

# 4. Update SettingsScreen
with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add onNavigateToMyOrders parameter
content = content.replace('    onLogout: () -> Unit\n) {', '    onLogout: () -> Unit,\n    onNavigateToMyOrders: () -> Unit = {}\n) {')

my_orders_item = """                SettingsItem(
                    icon = androidx.compose.material.icons.Icons.Filled.List,
                    title = "طلباتي",
                    subtitle = "تتبع حالة طلباتك من المتجر الزراعي",
                    onClick = onNavigateToMyOrders
                )
                
                SettingsItem(
                    icon = Icons.Filled.Person,"""

content = content.replace('import androidx.compose.material.icons.filled.Person', 'import androidx.compose.material.icons.filled.Person\nimport androidx.compose.material.icons.filled.List')

content = content.replace("""                SettingsItem(
                    icon = Icons.Filled.Person,""", my_orders_item)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/SettingsScreen.kt", "w") as f:
    f.write(content)
