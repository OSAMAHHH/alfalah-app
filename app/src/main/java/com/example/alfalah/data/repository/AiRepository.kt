package com.example.alfalah.data.repository

import com.example.alfalah.BuildConfig
import com.example.alfalah.data.model.AiChatRequest
import com.example.alfalah.data.model.AiChatResponse
import com.google.firebase.auth.FirebaseAuth
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit

class AiRepository {
    // URL for standard Android emulator local backend
    private val BASE_URL = BuildConfig.BACKEND_API_URL.takeIf { it.isNotEmpty() } ?: "http://10.0.2.2:3000/"

    private val apiService: AiApiService by lazy {
        val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        
        val client = OkHttpClient.Builder()
            .addInterceptor(logging)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()

        val moshi = Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()

        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
            .create(AiApiService::class.java)
    }

    suspend fun askAssistant(message: String, conversationId: String = ""): Pair<String, List<String>> = withContext(Dispatchers.IO) {
        try {
            val user = FirebaseAuth.getInstance().currentUser
            if (user == null) {
                return@withContext Pair("عذراً، يجب تسجيل الدخول أولاً.", emptyList())
            }
            
            // Get Firebase ID token
            val tokenResult = user.getIdToken(false).await()
            val token = "Bearer ${tokenResult.token}"

            val request = AiChatRequest(message = message, conversationId = conversationId)
            val response = apiService.sendMessage(token, request)
            
            Pair(response.answer, response.recommendedProducts)
        } catch (e: Exception) {
            // Provide a graceful fallback error message
            Pair("عذراً، لا يمكنني الاتصال بالخادم حالياً. يرجى التأكد من إعداد Backend بشكل صحيح. الخطأ: ${e.message}", emptyList())
        }
    }
}
