import re

with open("app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt", "r") as f:
    text = f.read()

new_weather_func = """
    suspend fun getCurrentWeather(): Result<WeatherInfo> = withContext(Dispatchers.IO) {
        try {
            var lat = 24.7136
            var lon = 46.6753
            var city = "الرياض (افتراضي)"
            
            try {
                // Get location via IP
                val ipRequest = Request.Builder().url("https://ipwho.is/").build()
                val ipResponse = client.newCall(ipRequest).execute()
                val bodyStr = ipResponse.body?.string()
                if (!bodyStr.isNullOrEmpty()) {
                    val ipData = JSONObject(bodyStr)
                    if (ipData.optBoolean("success", false)) {
                        lat = ipData.optDouble("latitude", 24.7136)
                        lon = ipData.optDouble("longitude", 46.6753)
                        city = ipData.optString("city", "الرياض")
                    }
                }
            } catch (e: Exception) {
                // Ignore IP lookup failure, use defaults
            }

            // Get weather via Open-Meteo
            val weatherUrl = "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&current=temperature_2m,is_day,weather_code"
            val weatherRequest = Request.Builder().url(weatherUrl).build()
            val weatherResponse = client.newCall(weatherRequest).execute()
            val bodyStr = weatherResponse.body?.string() ?: "{}"
            val weatherData = JSONObject(bodyStr)
            
            val current = weatherData.getJSONObject("current")
            val temp = current.getDouble("temperature_2m").toInt()
            val isDay = current.getInt("is_day") == 1
            val code = current.getInt("weather_code")
            val desc = getWeatherDescription(code)
            
            Result.success(WeatherInfo(temp, desc, isDay, code, city))
        } catch (e: Exception) {
            // Ultimate fallback if Open-Meteo fails
            Result.success(WeatherInfo(25, "غير متوفر", true, 0, "الطقس"))
        }
    }
"""

text = re.sub(r'suspend fun getCurrentWeather\(\): Result<WeatherInfo> = withContext\(Dispatchers\.IO\) \{[\s\S]*?private fun getWeatherDescription', new_weather_func + '\n    private fun getWeatherDescription', text)

with open("app/src/main/java/com/example/alfalah/data/repository/WeatherRepository.kt", "w") as f:
    f.write(text)
