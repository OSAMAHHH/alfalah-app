with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "r") as f:
    content = f.read()

models = """
@JsonClass(generateAdapter = true)
data class CartItem(
    val productId: String = "",
    val name: String = "",
    val price: Double = 0.0,
    val currency: String = "YER",
    val imageUrl: String = "",
    val quantity: Int = 1
)

@JsonClass(generateAdapter = true)
data class Order(
    @DocumentId val id: String = "",
    val userId: String = "",
    val customerName: String = "",
    val phone: String = "",
    val governorate: String = "",
    val address: String = "",
    val items: List<CartItem> = emptyList(),
    val totalAmount: Double = 0.0,
    val currency: String = "YER",
    val paymentMethod: String = "jeeb",
    val paymentReference: String = "",
    val paymentProofUrl: String = "",
    val paymentStatus: String = "pending", // pending, submitted, approved, rejected
    val orderStatus: String = "pending", // pending, processing, approved, rejected, completed, cancelled
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
)
"""

content = content + "\n" + models

# We also should add phone, governorate, address to User model if they don't exist
if "val phone: String" not in content:
    content = content.replace(
        'val photoUrl: String? = null',
        'val photoUrl: String? = null,\n    val phone: String = "",\n    val governorate: String = "",\n    val address: String = ""'
    )

with open("app/src/main/java/com/example/alfalah/data/model/Models.kt", "w") as f:
    f.write(content)
