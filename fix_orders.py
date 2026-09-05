import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

# Fix getMyOrders
old_query = """            val snapshot = firestore.collection("orders")
                .whereEqualTo("userId", uid)
                .orderBy("createdAt", Query.Direction.DESCENDING)
                .get().await()
            Result.success(snapshot.toObjects(Order::class.java))"""
            
new_query = """            val snapshot = firestore.collection("orders")
                .whereEqualTo("userId", uid)
                .get().await()
            val orders = snapshot.toObjects(Order::class.java).sortedByDescending { it.createdAt }
            Result.success(orders)"""

content = content.replace(old_query, new_query)

# Fix getAdminOrders
old_admin_query = """            val snapshot = firestore.collection("orders")
                .orderBy("createdAt", Query.Direction.DESCENDING)
                .get().await()
            Result.success(snapshot.toObjects(Order::class.java))"""

new_admin_query = """            val snapshot = firestore.collection("orders")
                .get().await()
            val orders = snapshot.toObjects(Order::class.java).sortedByDescending { it.createdAt }
            Result.success(orders)"""

content = content.replace(old_admin_query, new_admin_query)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
