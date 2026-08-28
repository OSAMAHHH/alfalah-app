package com.example.alfalah.ui.screens.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.filled.AdminPanelSettings
import androidx.compose.material.icons.filled.Store
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.repository.AuthRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.security.cert.X509Certificate

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    authRepository: AuthRepository,
    onNavigateToStore: () -> Unit,
    onNavigateToChat: () -> Unit,
    onNavigateToAdmin: () -> Unit,
    onLogout: () -> Unit
) {
    val currentUser by authRepository.currentUser.collectAsState()
    val scope = rememberCoroutineScope()
    var debugResult by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("مرحباً بك في الفلاح 🌱") },
                actions = {
                    IconButton(onClick = {
                        authRepository.logout()
                        onLogout()
                    }) {
                        Icon(Icons.AutoMirrored.Filled.Logout, contentDescription = "تسجيل خروج")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                "أهلاً ${currentUser?.name ?: ""}",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = onNavigateToChat,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(80.dp)
            ) {
                Icon(Icons.AutoMirrored.Filled.Chat, contentDescription = null, modifier = Modifier.size(32.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Text("اسأل المساعد الزراعي الذكي", style = MaterialTheme.typography.titleMedium)
            }

            Button(
                onClick = onNavigateToStore,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(80.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
            ) {
                Icon(Icons.Filled.Store, contentDescription = null, modifier = Modifier.size(32.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Text("متجر الأسمدة والمنتجات", style = MaterialTheme.typography.titleMedium)
            }

            if (currentUser?.role == "admin") {
                Spacer(modifier = Modifier.height(32.dp))
                FilledTonalButton(
                    onClick = onNavigateToAdmin,
                    modifier = Modifier.fillMaxWidth().height(60.dp)
                ) {
                    Icon(Icons.Filled.AdminPanelSettings, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("لوحة تحكم المشرف (Admin)")
                }
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
}
