package com.example.alfalah

import okhttp3.OkHttpClient
import okhttp3.Request
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import java.security.cert.X509Certificate

@RunWith(RobolectricTestRunner::class)
class TlsTest {
    @Test
    fun testHealthEndpoint() {
        println("A) Android -> /health: Testing...")
        val client = OkHttpClient.Builder().build()
        val request = Request.Builder()
            .url("https://alfalah-app-production.up.railway.app/health")
            .build()

        try {
            val response = client.newCall(request).execute()
            println("A) Android -> /health: ناجح (Success)")
            println("C) HTTP status: ${response.code}")
            println("D) HTTP client: OkHttp 4.10.0")
            println("E) Custom TLS config: None")
            
            try {
                val certs = response.handshake?.peerCertificates
                certs?.forEachIndexed { index, cert ->
                    if (cert is X509Certificate) {
                        println("   Cert $index: Issuer=${cert.issuerDN}, Subject=${cert.subjectDN}, ValidUntil=${cert.notAfter}")
                    }
                }
            } catch (e: Exception) {
                println("Could not get certs: ${e.message}")
            }
        } catch (e: Exception) {
            println("A) Android -> /health: فاشل (Failed)")
            println("B) Exception: ${e.javaClass.name}: ${e.message}")
            var cause = e.cause
            while (cause != null) {
                println("   Cause: ${cause.javaClass.name}: ${cause.message}")
                cause = cause.cause
            }
            println("C) HTTP status: N/A")
            println("D) HTTP client: OkHttp 4.10.0")
            println("E) Custom TLS config: None")
        }
    }
}
