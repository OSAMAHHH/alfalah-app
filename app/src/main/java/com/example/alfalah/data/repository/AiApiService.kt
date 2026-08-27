package com.example.alfalah.data.repository

import com.example.alfalah.data.model.AiChatRequest
import com.example.alfalah.data.model.AiChatResponse
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

interface AiApiService {
    @POST("api/ai/chat")
    suspend fun sendMessage(
        @Header("Authorization") token: String,
        @Body request: AiChatRequest
    ): AiChatResponse

    // TODO: Add multipart endpoint for image analysis when ready
    // @Multipart
    // @POST("api/ai/analyze-image")
    // suspend fun analyzeImage(@Part image: MultipartBody.Part, @Part("message") message: RequestBody): AiChatResponse
}
