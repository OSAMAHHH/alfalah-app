package com.example.alfalah.utils

object CurrencyUtils {
    fun formatPrice(price: Double, currency: String?): String {
        val safeCurrency = currency?.trim()?.uppercase() ?: ""
        val displayCurrency = when (safeCurrency) {
            "YER", "ر.ي" -> "ر.ي"
            "SAR" -> "ر.س"
            "USD", "$" -> "$"
            "" -> "ر.ي" // Fallback
            else -> currency
        }
        
        val formattedPrice = if (price % 1.0 == 0.0) {
            price.toLong().toString()
        } else {
            price.toString()
        }
        
        return "$formattedPrice $displayCurrency"
    }
}
