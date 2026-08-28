package com.example.alfalah.ui.screens.auth

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.repository.AuthRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.security.cert.X509Certificate

@Composable
fun LoginScreen(
    authRepository: AuthRepository,
    onNavigateToRegister: () -> Unit,
    onLoginSuccess: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    var debugResult by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("تسجيل الدخول", style = MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.height(32.dp))
        
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("البريد الإلكتروني") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("كلمة المرور") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        
        if (errorMsg != null) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(errorMsg!!, color = MaterialTheme.colorScheme.error)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = {
                scope.launch {
                    isLoading = true
                    errorMsg = null
                    val result = authRepository.login(email, password)
                    if (result.isSuccess) {
                        onLoginSuccess()
                    } else {
                        errorMsg = result.exceptionOrNull()?.message ?: "خطأ في تسجيل الدخول"
                    }
                    isLoading = false
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(modifier = Modifier.size(24.dp)) else Text("دخول")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        TextButton(onClick = onNavigateToRegister) {
            Text("ليس لديك حساب؟ سجل الآن")
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        
        // Debug TLS Button
        Button(
            onClick = {
                scope.launch {
                    debugResult = "جاري الفحص..."
                    debugResult = withContext(Dispatchers.IO) {
                        try {
                            val client = OkHttpClient.Builder().build()
                            val request = Request.Builder()
                                .url("https://alfalah-app-production.up.railway.app/health")
                                .build()
                            
                            val response = client.newCall(request).execute()
                            val sb = java.lang.StringBuilder()
                            sb.append("A) Android -> /health: SUCCESS\n")
                            sb.append("C) HTTP status: ${response.code}\n")
                            
                            val certs = response.handshake?.peerCertificates
                            sb.append("--- Certificates ---\n")
                            certs?.forEachIndexed { index, cert ->
                                if (cert is X509Certificate) {
                                    sb.append("[$index] Issuer: ${cert.issuerDN.name}\n")
                                    sb.append("    Subject: ${cert.subjectDN.name}\n")
                                }
                            }
                            sb.toString()
                        } catch (e: Exception) {
                            val sb = java.lang.StringBuilder()
                            sb.append("A) Android -> /health: FAILED\n")
                            sb.append("B) Exception: ${e.javaClass.name}\n")
                            sb.append("Message: ${e.message}\n")
                            
                            var cause = e.cause
                            var depth = 1
                            while (cause != null) {
                                sb.append("Cause $depth: ${cause.javaClass.name}: ${cause.message}\n")
                                cause = cause.cause
                                depth++
                            }
                            sb.toString()
                        }
                    }
                }
            },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
        ) {
            Text("Run TLS Diagnostics (DEBUG)")
        }
        
        if (debugResult.isNotEmpty()) {
            Surface(
                color = MaterialTheme.colorScheme.surfaceVariant,
                shape = MaterialTheme.shapes.small,
                modifier = Modifier.fillMaxWidth().padding(top = 16.dp)
            ) {
                Text(
                    text = debugResult,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}
