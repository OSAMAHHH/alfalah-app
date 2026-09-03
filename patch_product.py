import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

imports = """
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.outlined.FavoriteBorder
import com.example.alfalah.data.repository.UserServicesRepository
import kotlinx.coroutines.launch
import androidx.compose.ui.platform.LocalContext
import android.widget.Toast
"""

content = content.replace("import com.example.alfalah.ui.components.LoadingState", "import com.example.alfalah.ui.components.LoadingState" + imports)

# Add UserServicesRepository to parameters
content = content.replace("firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }", 
                          "firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },\n    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }")

# Add state and coroutine scope
state_code = """
    var product by remember { mutableStateOf<Product?>(null) }
    var isLoading by remember { mutableStateOf(true) }
    var isFavorite by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
"""
content = content.replace("    var product by remember { mutableStateOf<Product?>(null) }\n    var isLoading by remember { mutableStateOf(true) }", state_code)

# Check favorite on load
effect_code = """
    LaunchedEffect(productId) {
        val result = firestoreRepository.getProductById(productId)
        if (result.isSuccess) product = result.getOrNull()
        isFavorite = userServicesRepository.isFavorite(productId)
        isLoading = false
    }
"""
content = content.replace("""    LaunchedEffect(productId) {
        val result = firestoreRepository.getProductById(productId)
        if (result.isSuccess) product = result.getOrNull()
        isLoading = false
    }""", effect_code)

# Update TopAppBar to add actions
top_bar_old = """
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع") } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent)
"""
top_bar_new = """
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع") } },
                actions = {
                    if (product != null) {
                        IconButton(onClick = {
                            scope.launch {
                                if (isFavorite) {
                                    val res = userServicesRepository.removeFavorite(productId)
                                    if (res.isSuccess) {
                                        isFavorite = false
                                        Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                    }
                                } else {
                                    val res = userServicesRepository.addFavorite(productId, "product")
                                    if (res.isSuccess) {
                                        isFavorite = true
                                        Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                        }) {
                            Icon(
                                imageVector = if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                                contentDescription = "المفضلة",
                                tint = if (isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent)
"""
content = content.replace(top_bar_old, top_bar_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
