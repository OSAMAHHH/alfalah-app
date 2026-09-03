import re

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add routes
routes_old = """    const val PRODUCT_DETAILS = "product_details/{productId}"
    fun productDetails(id: String) = "product_details/$id"
}"""
routes_new = """    const val PRODUCT_DETAILS = "product_details/{productId}"
    fun productDetails(id: String) = "product_details/$id"
    const val CROP_DETAILS = "crop_details/{cropId}"
    fun cropDetails(id: String) = "crop_details/$id"
    const val PROBLEM_DETAILS = "problem_details/{problemId}"
    fun problemDetails(id: String) = "problem_details/$id"
}"""
content = content.replace(routes_old, routes_new)

# Add chat with initial query route
# We can just change ChatScreen composables to support initialQuery. Wait, ChatViewModel needs to read it.
# Actually, we can just use another route `chat_new?initialQuery={query}` or something.
# Let's check ChatViewModel.kt to see how to pass initial query.

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w", encoding="utf-8") as f:
    f.write(content)
