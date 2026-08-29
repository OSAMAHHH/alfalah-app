with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r") as f:
    text = f.read()

text = text.replace("    authRepository: AuthRepository,\n    onNavigateToStore: () -> Unit,", "    authRepository: AuthRepository,\n    weatherRepository: WeatherRepository = androidx.compose.runtime.remember { WeatherRepository() },\n    onNavigateToStore: () -> Unit,")

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(text)
