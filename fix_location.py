import re

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

location_logic = """
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }

    fun fetchWeather() {
        weatherLoading = true
        locationError = null
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED || ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            try {
                fusedLocationClient.getCurrentLocation(com.google.android.gms.location.Priority.PRIORITY_BALANCED_POWER_ACCURACY, null).addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                            if (weather == null) locationError = "فشل في جلب بيانات الطقس"
                            weatherLoading = false
                        }
                    } else {
                        // Fallback to lastLocation if getCurrentLocation is null
                        fusedLocationClient.lastLocation.addOnSuccessListener { lastLoc ->
                            if (lastLoc != null) {
                                scope.launch {
                                    weather = weatherRepository.getCurrentWeather(lastLoc.latitude, lastLoc.longitude).getOrNull()
                                    if (weather == null) locationError = "فشل في جلب بيانات الطقس"
                                    weatherLoading = false
                                }
                            } else {
                                locationError = "تعذر تحديد الموقع الجغرافي. تأكد من تفعيل الـ GPS."
                                weatherLoading = false
                            }
                        }.addOnFailureListener {
                            locationError = "تعذر تحديد الموقع الجغرافي."
                            weatherLoading = false
                        }
                    }
                }.addOnFailureListener {
                    locationError = "فشل في الحصول على الموقع."
                    weatherLoading = false
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
                weatherLoading = false
            }
        } else {
            locationError = "تحتاج لتفعيل صلاحية الموقع لعرض الطقس"
            weatherLoading = false
        }
    }
"""

old_location_logic = """
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }

    fun fetchWeather() {
        weatherLoading = true
        locationError = null
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                            if (weather == null) locationError = "فشل في جلب بيانات الطقس"
                            weatherLoading = false
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                        weatherLoading = false
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
                weatherLoading = false
            }
        } else {
            locationError = "فعّل الموقع لعرض الطقس في منطقتك"
            weatherLoading = false
        }
    }
"""

content = content.replace(old_location_logic.strip(), location_logic.strip())

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
