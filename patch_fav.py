import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/FavoritesScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

sig_old = """fun FavoritesScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,"""
sig_new = """fun FavoritesScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    onNavigateToCrop: (String) -> Unit = {},
    onNavigateToProblem: (String) -> Unit = {},"""
content = content.replace(sig_old, sig_new)

items_old = """                            when (item) {
                                is Crop -> CropCard(crop = item, userServicesRepository = userServicesRepository)
                                is AgriculturalProblem -> ProblemCard(problem = item, userServicesRepository = userServicesRepository)"""
items_new = """                            when (item) {
                                is Crop -> CropCard(crop = item, userServicesRepository = userServicesRepository, onClick = { onNavigateToCrop(item.id) })
                                is AgriculturalProblem -> ProblemCard(problem = item, userServicesRepository = userServicesRepository, onClick = { onNavigateToProblem(item.id) })"""
content = content.replace(items_old, items_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/FavoritesScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
