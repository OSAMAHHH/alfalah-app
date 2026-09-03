import re

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

mc_old = """    LaunchedEffect(Unit) {
        val res = userServicesRepository.getMyCrops()
        if (res.isSuccess) {
            val cropsData = res.getOrDefault(emptyList())
            myCrops = cropsData
            
            // Fetch crop details
            val fullCrops = mutableListOf<Crop>()
            for (myCrop in cropsData) {
                val cres = firestoreRepository.getCropById(myCrop.cropId)
                cres.getOrNull()?.let { fullCrops.add(it) }
            }
            loadedCrops = fullCrops
        }
        isLoading = false
    }"""
mc_new = """    LaunchedEffect(Unit) {
        val cropsData = userServicesRepository.getMyCrops()
        myCrops = cropsData
        
        // Fetch crop details
        val fullCrops = mutableListOf<Crop>()
        for (myCrop in cropsData) {
            val cres = firestoreRepository.getCropById(myCrop.cropId)
            cres.getOrNull()?.let { fullCrops.add(it) }
        }
        loadedCrops = fullCrops
        isLoading = false
    }"""
content = content.replace(mc_old, mc_new)

with open("app/src/main/java/com/example/alfalah/ui/screens/profile/MyCropsScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
