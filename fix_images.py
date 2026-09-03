import re

def fix_file(path, is_store=False):
    with open(path, "r") as f:
        content = f.read()
    
    if "import coil.compose.SubcomposeAsyncImage" not in content:
        content = content.replace("import coil.compose.AsyncImage", "import coil.compose.AsyncImage\nimport coil.compose.SubcomposeAsyncImage\nimport androidx.compose.material3.CircularProgressIndicator")
        
    old_async = r'AsyncImage\(model = product\??\.imageUrl, contentDescription = null, modifier = Modifier\.fillMaxSize\(\), contentScale = ContentScale\.Crop\)'
    new_subcompose = """SubcomposeAsyncImage(
                        model = product?.imageUrl if "?." in "product?.imageUrl" else product.imageUrl,
                        contentDescription = null,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop,
                        loading = {
                            androidx.compose.foundation.layout.Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                                CircularProgressIndicator(modifier = Modifier.size(24.dp))
                            }
                        },
                        error = {
                            androidx.compose.material3.Icon(androidx.compose.material.icons.Icons.Outlined.ImageNotSupported, contentDescription = null, modifier = Modifier.size(48.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                        }
                    )"""
                    
    if is_store:
        new_subcompose = new_subcompose.replace("product?.imageUrl if \"?.\" in \"product?.imageUrl\" else product.imageUrl", "product.imageUrl")
        new_subcompose = new_subcompose.replace("Icons.Outlined.ImageNotSupported", "androidx.compose.material.icons.Icons.Outlined.ImageNotSupported")
    else:
        new_subcompose = new_subcompose.replace("product?.imageUrl if \"?.\" in \"product?.imageUrl\" else product.imageUrl", "product?.imageUrl")
        new_subcompose = new_subcompose.replace("Icons.Outlined.ImageNotSupported", "androidx.compose.material.icons.Icons.Outlined.ImageNotSupported")

    content = re.sub(old_async, new_subcompose, content)
    
    # Also fix Icons.Outlined.ImageNotSupported import if missing
    if "androidx.compose.material.icons.outlined.ImageNotSupported" not in content:
        content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.outlined.ImageNotSupported")
        
    with open(path, "w") as f:
        f.write(content)

fix_file("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", True)
fix_file("app/src/main/java/com/example/alfalah/ui/screens/store/ProductDetailsScreen.kt", False)

