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
import retrofit2.HttpException
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.io.IOException
import java.net.SocketTimeoutException 
import java.util.concurrent.TimeUnit
import org.json.JSONObject
import android.util.Log

class AiRepository {
    private val firestoreRepo = FirestoreRepository()


    // URL for standard Android emulator local backend
    private val BASE_URL = BuildConfig.BACKEND_API_URL.takeIf { it.isNotEmpty() } ?: "http://10.0.2.2:3000/"

    private val apiService: AiApiService by lazy {
        val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        
        val client = OkHttpClient.Builder()
            .addInterceptor(logging)
            .connectTimeout(60, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
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

    suspend fun askAssistant(message: String, history: List<com.example.alfalah.data.model.ChatMessageItem> = emptyList(), conversationId: String = ""): Pair<String, List<String>> = withContext(Dispatchers.IO) {
        try {
            val user = FirebaseAuth.getInstance().currentUser
            if (user == null) {
                return@withContext Pair("عذراً، يجب تسجيل الدخول أولاً.", emptyList())
            }
            
            // Get Firebase ID token
            val tokenResult = user.getIdToken(false).await()
            val token = "Bearer ${tokenResult.token}"

            // ---- Local Knowledge Base Search ----
            val lowerMsg = message.lowercase()
            val crops = firestoreRepo.getCrops().getOrNull() ?: emptyList()
            val problems = firestoreRepo.getProblems().getOrNull() ?: emptyList()
            
            val matchedProblem = problems.find { p ->
                lowerMsg.contains(p.name.lowercase()) || p.synonyms.any { lowerMsg.contains(it.lowercase()) }
            }
            if (matchedProblem != null) {
                val ans = "بناءً على قاعدة المعرفة المحلية:\nالمشكلة: ${matchedProblem.name}\nالأعراض: ${matchedProblem.symptoms.joinToString("، ")}\nالعلاج: ${matchedProblem.treatment}"
                return@withContext Pair(ans, matchedProblem.recommendedProductIds)
            }
            
            val matchedCrop = crops.find { c ->
                lowerMsg.contains(c.name.lowercase()) || c.synonyms.any { lowerMsg.contains(it.lowercase()) }
            }
            if (matchedCrop != null) {
                val ans = "بناءً على قاعدة المعرفة المحلية:\nالمحصول: ${matchedCrop.name}\nالوصف: ${matchedCrop.description}\nموسم الزراعة: ${matchedCrop.plantingSeason}\nطرق الري: ${matchedCrop.irrigation}\nالتسميد: ${matchedCrop.fertilization}"
                return@withContext Pair(ans, emptyList())
            }
            // ---- End Local Search ----



            val request = AiChatRequest(message = message, conversationId = conversationId, history = history)
            
            val fullUrl = if (BASE_URL.endsWith("/")) "${BASE_URL}api/ai/chat" else "${BASE_URL}/api/ai/chat"
            Log.d("AI_DEBUG", "BASE_URL: $BASE_URL")
            Log.d("AI_DEBUG", "Preparing to call backend endpoint: api/ai/chat")
            Log.d("AI_DEBUG", "Final URL: $fullUrl")
            
            val response = apiService.sendMessage(token, request)
            
            Pair(response.answer, response.recommendedProducts)

        } catch (e: HttpException) {
            Log.e("AI_DEBUG", "HttpException - Status Code: ${e.code()}, URL: ${e.response()?.raw()?.request?.url}")
            val errorMessage = when (e.code()) {
                401, 403 -> "مشكلة في المصادقة. يرجى تسجيل الدخول مجدداً."
                429 -> {
                    try {
                        val errorBody = e.response()?.errorBody()?.string()
                        val json = JSONObject(errorBody ?: "")
                        json.optString("error", "تجاوزت حد الاستخدام أو يوجد ضغط كبير. يرجى المحاولة بعد قليل.")
                    } catch (ex: Exception) {
                        "تجاوزت حد الاستخدام أو يوجد ضغط كبير. يرجى المحاولة بعد قليل."
                    }
                }
                503 -> {
                    try {
                        val errorBody = e.response()?.errorBody()?.string()
                        val json = JSONObject(errorBody ?: "")
                        json.optString("error", "خوادم الذكاء الاصطناعي غير متاحة مؤقتاً. يرجى المحاولة لاحقاً.")
                    } catch (ex: Exception) {
                        "خوادم الذكاء الاصطناعي غير متاحة مؤقتاً. يرجى المحاولة لاحقاً."
                    }
                }
                500 -> "حدث خطأ داخلي في الخادم."
                else -> "حدث خطأ غير متوقع (${e.code()}). يرجى المحاولة لاحقاً."
            }
            Pair(errorMessage, emptyList())
        } catch (e: SocketTimeoutException) {
            Pair("انتهى وقت الاتصال. يرجى التحقق من جودة الإنترنت لديك والمحاولة مجدداً.", emptyList())
        } catch (e: IOException) {
            val fullUrl = if (BASE_URL.endsWith("/")) "${BASE_URL}api/ai/chat" else "${BASE_URL}/api/ai/chat"
            Log.e("AI_DEBUG", "IOException: ${e.javaClass.name}, Message: ${e.message}, BASE_URL: $BASE_URL, Final URL: $fullUrl")
            Pair("عذراً، لا يمكنني الاتصال بالخادم حالياً. يرجى التأكد من اتصالك بالإنترنت.", emptyList())
        } catch (e: Exception) {
            val fullUrl = if (BASE_URL.endsWith("/")) "${BASE_URL}api/ai/chat" else "${BASE_URL}/api/ai/chat"
            Log.e("AI_DEBUG", "Exception: ${e.javaClass.name}, Message: ${e.message}, BASE_URL: $BASE_URL, Final URL: $fullUrl")
            Pair("عذراً، حدث خطأ غير متوقع: ${e.message}", emptyList())
        }
    }
}
