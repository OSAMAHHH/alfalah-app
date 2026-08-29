package com.example.alfalah.ui.screens.guide

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.AgriculturalProblem
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GuideScreen(
    category: String,
    onBack: () -> Unit,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var isLoading by remember { mutableStateOf(true) }
    var items by remember { mutableStateOf<List<Any>>(emptyList()) }
    val scope = rememberCoroutineScope()

    val title = when (category) {
        "crops" -> "دليل المحاصيل"
        "pests" -> "دليل الآفات والأمراض"
        "irrigation" -> "دليل الري"
        else -> "الدليل الزراعي"
    }

    LaunchedEffect(category) {
        isLoading = true
        when (category) {
            "crops" -> {
                val res = firestoreRepository.getCrops()
                items = res.getOrDefault(emptyList())
            }
            "pests" -> {
                val res = firestoreRepository.getProblems()
                items = res.getOrDefault(emptyList())
            }
            "irrigation" -> {
                // Mock for irrigation until proper collection exists
                items = emptyList()
            }
        }
        isLoading = false
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(title, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                    }
                }
            )
        }
    ) { padding ->
        if (isLoading) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else if (items.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text(
                    text = if (category == "irrigation") "سيتم إضافة دليل الري قريباً" else "لا توجد بيانات متاحة حالياً",
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(items) { item ->
                    when (item) {
                        is Crop -> CropCard(item)
                        is AgriculturalProblem -> ProblemCard(item)
                    }
                }
            }
        }
    }
}

@Composable
fun CropCard(crop: Crop) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(crop.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
            if (crop.description.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(crop.description, style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
fun ProblemCard(problem: AgriculturalProblem) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(problem.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onErrorContainer)
            Spacer(modifier = Modifier.height(8.dp))
            Text("النوع: ${problem.type}", style = MaterialTheme.typography.labelMedium)
            if (problem.symptoms.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text("الأعراض: ${problem.symptoms.joinToString(", ")}", style = MaterialTheme.typography.bodyMedium)
            }
            if (problem.treatment.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text("العلاج: ${problem.treatment}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold)
            }
        }
    }
}
