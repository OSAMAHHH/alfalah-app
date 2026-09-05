import re

with open("app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt", "r") as f:
    content = f.read()

# Add Context import if not exists
if "import android.content.Context" not in content:
    content = content.replace("import org.json.JSONObject", "import org.json.JSONObject\nimport android.content.Context\nimport android.location.Geocoder\nimport java.util.Locale")

# Change getCurrentWeather signature
content = content.replace(
    "suspend fun getCurrentWeather(lat: Double, lon: Double): Result<WeatherInfo>",
    "suspend fun getCurrentWeather(lat: Double, lon: Double, context: Context): Result<WeatherInfo>"
)

# Update location logic
old_weather_logic = '''            val desc = getWeatherDescription(code)
            
            Result.success(WeatherInfo(temp, desc, isDay, code, "الموقع الحالي"))
        } catch (e: Exception) {
            Result.success(WeatherInfo(25, "غير متوفر", true, 0, "الموقع الحالي"))
        }'''

new_weather_logic = '''            val desc = getWeatherDescription(code)
            
            var cityName = "الموقع الحالي"
            try {
                val geocoder = Geocoder(context, Locale("ar"))
                val addresses = geocoder.getFromLocation(lat, lon, 1)
                if (!addresses.isNullOrEmpty()) {
                    val address = addresses[0]
                    val locality = address.locality ?: address.subAdminArea ?: address.adminArea
                    val countryName = address.countryName
                    if (locality != null && countryName != null) {
                        cityName = "$locality، $countryName"
                    } else if (locality != null) {
                        cityName = locality
                    } else if (countryName != null) {
                        cityName = countryName
                    }
                }
            } catch (e: Exception) {
                // Ignore geocoder errors and fallback to default
            }
            
            Result.success(WeatherInfo(temp, desc, isDay, code, cityName))
        } catch (e: Exception) {
            Result.success(WeatherInfo(25, "غير متوفر", true, 0, "الموقع الحالي"))
        }'''

content = content.replace(old_weather_logic, new_weather_logic)

with open("app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r") as f:
    hs_content = f.read()

hs_content = hs_content.replace(
    'weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()',
    'weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude, context).getOrNull()'
)

hs_content = hs_content.replace(
    'weather = weatherRepository.getCurrentWeather(lastLoc.latitude, lastLoc.longitude).getOrNull()',
    'weather = weatherRepository.getCurrentWeather(lastLoc.latitude, lastLoc.longitude, context).getOrNull()'
)

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(hs_content)
