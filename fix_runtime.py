import re

# Fix 1: AiRepository.kt - BACKEND_API_URL
with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "r") as f:
    ai_content = f.read()
# Replace default 10.0.2.2 with the actual deployed cloud run URL
ai_content = ai_content.replace('"http://10.0.2.2:3000/"', '"https://ais-dev-zzuaevc44nndlouy6altyk-955191457297.europe-west2.run.app/"')
with open("app/src/main/java/com/example/alfalah/data/repository/AiRepository.kt", "w") as f:
    f.write(ai_content)

# Fix 2: firestore.rules - Cart PERMISSION_DENIED
with open("firestore.rules", "r") as f:
    rules = f.read()

# Add a wildcard explicitly for subcollections of user
old_user_match = """    match /users/{userId} {
      allow read, write: if isAuthenticated() && (request.auth.uid == userId || isAdmin());"""
new_user_match = """    match /users/{userId} {
      allow read, write: if isAuthenticated() && (request.auth.uid == userId || isAdmin());
      
      // Explicit wildcard for all subcollections to guarantee cart/favorites/etc are writable
      match /{document=**} {
        allow read, write: if isAuthenticated() && (request.auth.uid == userId || isAdmin());
      }"""
if "match /{document=**}" not in rules.split("match /users/{userId}")[1].split("match /products")[0]:
    rules = rules.replace(old_user_match, new_user_match)

with open("firestore.rules", "w") as f:
    f.write(rules)

# Fix 3: storage.rules - Product images not showing for clients
# (because images were uploaded to images/ before my fix, which falls under {allPaths=**} read: if request.auth != null)
with open("storage.rules", "r") as f:
    storage_rules = f.read()

old_storage = """    match /products/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }"""
new_storage = """    match /products/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    match /images/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }"""
if "match /images/{allPaths=**}" not in storage_rules:
    storage_rules = storage_rules.replace(old_storage, new_storage)

with open("storage.rules", "w") as f:
    f.write(storage_rules)

# Fix 4: AppNavigation.kt - Crops/Problems disappearance
with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "r") as f:
    nav_content = f.read()

nav_content = nav_content.replace('Pair("guide", "الدليل")', 'Pair("guide/crops", "الدليل")')
nav_content = nav_content.replace('onNavigateToGuide = { category -> navController.navigate("guide") }', 'onNavigateToGuide = { category -> navController.navigate("guide/$category") }')

old_guide_route = """            composable("guide") {
                GuideScreen(
                    category = "crops","""
new_guide_route = """            composable(
                route = "guide/{category}",
                arguments = listOf(navArgument("category") { type = NavType.StringType; defaultValue = "crops" })
            ) { backStackEntry ->
                val category = backStackEntry.arguments?.getString("category") ?: "crops"
                GuideScreen(
                    category = category,"""
if "guide/{category}" not in nav_content:
    nav_content = nav_content.replace(old_guide_route, new_guide_route)

# Add navArgument and NavType imports if missing
if "androidx.navigation.navArgument" not in nav_content:
    nav_content = "import androidx.navigation.navArgument\nimport androidx.navigation.NavType\n" + nav_content

with open("app/src/main/java/com/example/alfalah/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(nav_content)

# Update build.gradle.kts Version
with open("app/build.gradle.kts", "r") as f:
    build_content = f.read()

build_content = build_content.replace('versionCode = 2', 'versionCode = 3')
build_content = build_content.replace('versionName = "1.0.1-Build-20260905"', 'versionName = "1.0.2-RuntimeFix"')

with open("app/build.gradle.kts", "w") as f:
    f.write(build_content)

