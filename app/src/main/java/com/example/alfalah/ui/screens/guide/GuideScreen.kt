package com.example.alfalah.ui.screens.guide


import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search

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

import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import com.example.alfalah.data.repository.UserServicesRepository
import kotlinx.coroutines.launch
import androidx.compose.ui.platform.LocalContext
import android.widget.Toast

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.foundation.shape.RoundedCornerShape
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
    onNavigateToCrop: (String) -> Unit = {},
    onNavigateToProblem: (String) -> Unit = {},
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() }
) {
    var isLoading by remember { mutableStateOf(true) }
    var items by remember { mutableStateOf<List<Any>>(emptyList()) }
    var lastDoc by remember { mutableStateOf<com.google.firebase.firestore.DocumentSnapshot?>(null) }
    var searchQuery by remember { mutableStateOf("") }
    var selectedFilter by remember { mutableStateOf("الكل") }
    var hasMore by remember { mutableStateOf(true) }
    var isLoadingMore by remember { mutableStateOf(false) }
    var errorMsg by remember { mutableStateOf<String?>(null) }


    val filteredItems = remember(items, searchQuery, selectedFilter) {
        items.filter { item ->
            val matchesSearch = if (searchQuery.isBlank()) true else {
                when (item) {
                    is Crop -> {
                        item.name.contains(searchQuery, ignoreCase = true) ||
                        item.synonyms.any { it.contains(searchQuery, ignoreCase = true) } ||
                        item.description.contains(searchQuery, ignoreCase = true)
                    }
                    is AgriculturalProblem -> {
                        item.name.contains(searchQuery, ignoreCase = true) ||
                        item.synonyms.any { it.contains(searchQuery, ignoreCase = true) } ||
                        item.symptoms.any { it.contains(searchQuery, ignoreCase = true) }
                    }
                    else -> false
                }
            }
            
            val matchesFilter = if (selectedFilter == "الكل") true else {
                val englishFilter = when (selectedFilter) {
                    "الأمراض" -> listOf("disease", "أمراض", "مرض")
                    "الآفات" -> listOf("pest", "آفات", "آفة")
                    "نقص العناصر الغذائية" -> listOf("deficiency", "nutrient_deficiency", "نقص")
                    "مشاكل أخرى" -> listOf("other", "irrigation_problem", "soil_problem", "أخرى")
                    else -> listOf(selectedFilter)
                }
                when (item) {
                    is AgriculturalProblem -> englishFilter.any { item.type.equals(it, ignoreCase = true) } || englishFilter.any { item.type.contains(it, ignoreCase = true) }
                    else -> true
                }
            }
            
            matchesSearch && matchesFilter
        }
    }
    
    val problemFilters = listOf("الكل", "الأمراض", "الآفات", "نقص العناصر الغذائية", "مشاكل أخرى")

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
                Column(modifier = Modifier.fillMaxSize().padding(padding), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                    com.example.alfalah.ui.components.EmptyState(
                        icon = Icons.Filled.Eco,
                        title = "لا توجد بيانات",
                        message = errorMsg ?: "لا توجد بيانات متاحة حالياً، يرجى التأكد من اتصالك بالإنترنت.",
                        modifier = Modifier.weight(1f)
                    )
                    if (errorMsg != null) {
                        Button(onClick = { loadData(false) }, modifier = Modifier.padding(bottom = 32.dp)) {
                            Text("إعادة المحاولة")
                        }
                    }
                }
            }
        } else {
            Column(modifier = Modifier.fillMaxSize().padding(padding)) {
                // Search Bar
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                    placeholder = { Text("ابحث هنا...") },
                    leadingIcon = { Icon(Icons.Filled.Search, contentDescription = "بحث") },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Filled.Clear, contentDescription = "مسح البحث")
                            }
                        }
                    },
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surface,
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    ),
                    singleLine = true
                )
                
                // Filters
                if (category == "pests") {
                    LazyRow(
                        modifier = Modifier.fillMaxWidth(),
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(problemFilters) { filter ->
                            FilterChip(
                                selected = selectedFilter == filter,
                                onClick = { selectedFilter = filter },
                                label = { Text(filter) }
                            )
                        }
                    }
                }
                
                if (filteredItems.isEmpty() && !isLoading) {
                    Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("لم نجد نتائج مطابقة", style = MaterialTheme.typography.titleMedium)
                            if (hasMore) {
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { loadData(true) }) {
                                    Text("تحميل المزيد من البيانات")
                                }
                            }
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.weight(1f).fillMaxWidth(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(filteredItems.size) { index ->
                            val item = filteredItems[index]
                            when (item) {
                                is Crop -> CropCard(item, onClick = { onNavigateToCrop(item.id) })
                                is AgriculturalProblem -> ProblemCard(item, onClick = { onNavigateToProblem(item.id) })
                            }
                            
                            // Auto load more when reaching bottom of original items
                            if (index == filteredItems.size - 1 && hasMore && !isLoadingMore) {
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
    }
}

@Composable
fun CropCard(
    crop: Crop, 
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    onClick: () -> Unit = {}
) {
    var isFavorite by remember { mutableStateOf(false) }
    var isMyCrop by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    
    LaunchedEffect(crop.id) {
        isFavorite = userServicesRepository.isFavorite(crop.id)
        isMyCrop = userServicesRepository.isMyCrop(crop.id)
    }

    Card(
        modifier = Modifier.fillMaxWidth().clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(crop.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = {
                        scope.launch {
                            if (isFavorite) {
                                if (userServicesRepository.removeFavorite(crop.id).isSuccess) {
                                    isFavorite = false
                                    Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                }
                            } else {
                                if (userServicesRepository.addFavorite(crop.id, "crop").isSuccess) {
                                    isFavorite = true
                                    Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    }) {
                        Icon(if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder, contentDescription = "المفضلة", tint = if (isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
        }
    }
}

@Composable
fun ProblemCard(
    problem: AgriculturalProblem, 
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() },
    onClick: () -> Unit = {}
) {
    var isFavorite by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    
    LaunchedEffect(problem.id) {
        isFavorite = userServicesRepository.isFavorite(problem.id)
    }

    Card(
        modifier = Modifier.fillMaxWidth().clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(problem.name, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onErrorContainer, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = {
                        scope.launch {
                            if (isFavorite) {
                                if (userServicesRepository.removeFavorite(problem.id).isSuccess) {
                                    isFavorite = false
                                    Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                }
                            } else {
                                if (userServicesRepository.addFavorite(problem.id, "problem").isSuccess) {
                                    isFavorite = true
                                    Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    }) {
                        Icon(if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder, contentDescription = "المفضلة", tint = if (isFavorite) MaterialTheme.colorScheme.onErrorContainer else MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
            Text(problem.type, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))
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
