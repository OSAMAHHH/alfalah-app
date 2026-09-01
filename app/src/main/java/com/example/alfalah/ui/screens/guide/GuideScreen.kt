package com.example.alfalah.ui.screens.guide

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material.icons.filled.Eco
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
    var lastDoc by remember { mutableStateOf<com.google.firebase.firestore.DocumentSnapshot?>(null) }
    var hasMore by remember { mutableStateOf(true) }
    var isLoadingMore by remember { mutableStateOf(false) }
    var errorMsg by remember { mutableStateOf<String?>(null) }

    val title = when (category) {
        "crops" -> "دليل المحاصيل"
        "pests" -> "دليل الآفات والأمراض"
        "irrigation" -> "دليل الري"
        else -> "الدليل الزراعي"
    }

    fun loadData(isLoadMore: Boolean = false) {
        if (!hasMore && isLoadMore) return
        if (isLoadMore) isLoadingMore = true else isLoading = true
        
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
            try {
                when (category) {
                    "crops" -> {
                        val res = firestoreRepository.getCropsPaginated(15, if (isLoadMore) lastDoc else null)
                        if (res.isSuccess) {
                            val (newItems, nextDoc) = res.getOrThrow()
                            items = if (isLoadMore) items + newItems else newItems
                            lastDoc = nextDoc
                            hasMore = nextDoc != null
                            errorMsg = null
                        } else {
                            if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                        }
                    }
                    "pests" -> {
                        val res = firestoreRepository.getProblemsPaginated(15, if (isLoadMore) lastDoc else null)
                        if (res.isSuccess) {
                            val (newItems, nextDoc) = res.getOrThrow()
                            items = if (isLoadMore) items + newItems else newItems
                            lastDoc = nextDoc
                            hasMore = nextDoc != null
                            errorMsg = null
                        } else {
                            if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
                        }
                    }
                    "irrigation" -> {
                        items = emptyList()
                        hasMore = false
                    }
                }
            } catch (e: Exception) {
                if (!isLoadMore) errorMsg = "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت."
            } finally {
                if (isLoadMore) isLoadingMore = false else isLoading = false
            }
        }
    }

    LaunchedEffect(category) {
        items = emptyList()
        lastDoc = null
        hasMore = true
        loadData(false)
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
            com.example.alfalah.ui.components.LoadingState(modifier = Modifier.padding(padding))
        } else if (items.isEmpty()) {
            if (category == "irrigation") {
                com.example.alfalah.ui.components.EmptyState(
                    icon = Icons.Filled.WaterDrop,
                    title = "قريباً",
                    message = "سيتم إضافة دليل الري قريباً",
                    modifier = Modifier.padding(padding)
                )
            } else {
                com.example.alfalah.ui.components.EmptyState(
                    icon = Icons.Filled.Eco,
                    title = "لا توجد بيانات",
                    message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                    modifier = Modifier.padding(padding)
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(items.size) { index ->
                    val item = items[index]
                    when (item) {
                        is Crop -> CropCard(item as Crop)
                        is AgriculturalProblem -> ProblemCard(item as AgriculturalProblem)
                    }
                    
                    if (index == items.size - 1 && hasMore && !isLoadingMore) {
                        LaunchedEffect(index) {
                            loadData(true)
                        }
                    }
                }
                
                if (isLoadingMore) {
                    item {
                        Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                            CircularProgressIndicator(modifier = Modifier.size(32.dp), color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CropCard(crop: Crop) {
    var expanded by remember { mutableStateOf(false) }
    Card(
        modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(crop.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Icon(if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            }
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = tween(300)),
                exit = shrinkVertically(animationSpec = tween(300))
            ) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    if (crop.description.isNotEmpty()) DetailSection("الوصف", crop.description)
                    if (crop.plantingSeason.isNotEmpty()) DetailSection("موسم الزراعة", crop.plantingSeason)
                    if (crop.soil.isNotEmpty()) DetailSection("التربة المناسبة", crop.soil)
                    if (crop.irrigation.isNotEmpty()) DetailSection("إرشادات الري", crop.irrigation)
                    if (crop.fertilization.isNotEmpty()) DetailSection("إرشادات التسميد", crop.fertilization)
                    if (crop.notes.isNotEmpty()) DetailSection("ملاحظات هامة", crop.notes)
                }
            }
        }
    }
}

@Composable
fun ProblemCard(problem: AgriculturalProblem) {
    var expanded by remember { mutableStateOf(false) }
    Card(
        modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(problem.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onErrorContainer, fontWeight = FontWeight.Bold)
                Icon(if (expanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore, contentDescription = null, tint = MaterialTheme.colorScheme.onErrorContainer)
            }
            Text(problem.type, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))
            
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = tween(300)),
                exit = shrinkVertically(animationSpec = tween(300))
            ) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    if (problem.symptoms.isNotEmpty()) DetailSection("الأعراض", problem.symptoms.joinToString("، "))
                    if (problem.causes.isNotEmpty()) DetailSection("الأسباب", problem.causes)
                    if (problem.prevention.isNotEmpty()) DetailSection("طرق الوقاية", problem.prevention)
                    if (problem.treatment.isNotEmpty()) DetailSection("العلاج", problem.treatment)
                }
            }
        }
    }
}

@Composable
fun DetailSection(title: String, content: String) {
    Column(modifier = Modifier.padding(bottom = 12.dp)) {
        Text(title, style = MaterialTheme.typography.titleSmall, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(4.dp))
        Text(content, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
    }
}
