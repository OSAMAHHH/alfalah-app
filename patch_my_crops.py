import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

sig_old = """fun MyCropsScreen(
    onBack: () -> Unit,"""
sig_new = """fun MyCropsScreen(
    onBack: () -> Unit,
    onNavigateToCrop: (String) -> Unit = {},"""
content = content.replace(sig_old, sig_new)

effect_old = """    LaunchedEffect(Unit) {
        val cropsData = userServicesRepository.getMyCrops()
        myCrops = cropsData
        
        // Fetch crop details
        val fullCrops = mutableListOf<Crop>()
        for (myCrop in cropsData) {
            val res = firestoreRepository.getCropById(myCrop.cropId)
            res.getOrNull()?.let { fullCrops.add(it) }
        }
        loadedCrops = fullCrops
        isLoading = false
    }"""
    
effect_new = """    LaunchedEffect(Unit) {
        val res = userServicesRepository.getMyCrops()
        if (res.isSuccess) {
            val cropsData = res.getOrDefault(emptyList())
            myCrops = cropsData
            
            // Fetch crop details
            val fullCrops = mutableListOf<Crop>()
            for (myCrop in cropsData) {
                val cres = firestoreRepository.getCropById(myCrop.itemId) // MyCrop uses itemId actually, let's check
                cres.getOrNull()?.let { fullCrops.add(it) }
            }
            loadedCrops = fullCrops
        }
        isLoading = false
    }"""
content = content.replace(effect_old, effect_new)

items_old = "CropCard(crop = loadedCrops[index], userServicesRepository = userServicesRepository)"
items_new = "CropCard(crop = loadedCrops[index], userServicesRepository = userServicesRepository, onClick = { onNavigateToCrop(loadedCrops[index].id) })"
content = content.replace(items_old, items_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
