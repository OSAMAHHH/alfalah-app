with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()
    
content = content.replace("val itemRoute = it.first", "val itemRoute = it.first.first")

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "r") as f:
    content = f.read()
    
old_disposable = """    // Refresh cart count every time screen becomes active (or just rely on local state updates)
    androidx.compose.runtime.DisposableEffect(androidx.lifecycle.compose.LocalLifecycleOwner.current) {
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->
            if (event == androidx.lifecycle.Lifecycle.Event.ON_RESUME) {
                refreshCart()
            }
        }
        val lifecycle = androidx.lifecycle.compose.LocalLifecycleOwner.current.lifecycle
        lifecycle.addObserver(observer)
        onDispose {
            lifecycle.removeObserver(observer)
        }
    }"""
    
new_disposable = """    // Refresh cart count every time screen becomes active (or just rely on local state updates)
    val lifecycleOwner = androidx.lifecycle.compose.LocalLifecycleOwner.current
    androidx.compose.runtime.DisposableEffect(lifecycleOwner) {
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->
            if (event == androidx.lifecycle.Lifecycle.Event.ON_RESUME) {
                refreshCart()
            }
        }
        val lifecycle = lifecycleOwner.lifecycle
        lifecycle.addObserver(observer)
        onDispose {
            lifecycle.removeObserver(observer)
        }
    }"""
    
content = content.replace(old_disposable, new_disposable)
with open("app/src/main/java/com/example/alfalah/ui/screens/store/StoreScreen.kt", "w") as f:
    f.write(content)
