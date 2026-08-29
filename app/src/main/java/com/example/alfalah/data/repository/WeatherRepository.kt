package com.example.alfalah.data.repository

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

data class WeatherInfo(
    val temperature: Int,
    val description: String,
    val isDay: Boolean,
    val code: Int,
    val city: String
)

class WeatherRepository {
    private val client = OkHttpClient()

    suspend fun getCurrentWeather(): Result<WeatherInfo> = withContext(Dispatchers.IO) {
        try {
            // Get location via IP
            val ipRequest = Request.Builder().url("http://ip-api.com/json").build()
            val ipResponse = client.newCall(ipRequest).execute()
            val ipData = JSONObject(ipResponse.body?.string() ?: "{}")
            
            val lat = ipData.optDouble("lat", 24.7136) // Default Riyadh
            val lon = ipData.optDouble("lon", 46.6753)
            val city = ipData.optString("city", "الرياض")

            // Get weather via Open-Meteo
            val weatherUrl = "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&current=temperature_2m,is_day,weather_code"
            val weatherRequest = Request.Builder().url(weatherUrl).build()
            val weatherResponse = client.newCall(weatherRequest).execute()
            val weatherData = JSONObject(weatherResponse.body?.string() ?: "{}")
            
            val current = weatherData.getJSONObject("current")
            val temp = current.getDouble("temperature_2m").toInt()
            val isDay = current.getInt("is_day") == 1
            val code = current.getInt("weather_code")

            val desc = getWeatherDescription(code)
            
            Result.success(WeatherInfo(temp, desc, isDay, code, city))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun getWeatherDescription(code: Int): String {
        return when (code) {
            0 -> "صافي"
            1, 2, 3 -> "غائم جزئياً"
            45, 48 -> "ضبابي"
            51, 53, 55 -> "رذاذ"
            61, 63, 65 -> "ممطر"
            71, 73, 75 -> "ثلوج"
            80, 81, 82 -> "زخات مطر"
            95, 96, 99 -> "عاصفة رعدية"
            else -> "غير معروف"
        }
    }
}
