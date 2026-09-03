package com.example.alfalah.ui.screens.guide

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.SmartToy
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.AgriculturalProblem
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.repository.FirestoreRepository
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.LoadingState
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CropDetailsScreen(
    cropId: String,
    onBack: () -> Unit,
    onNavigateToProblem: (String) -> Unit,
    onNavigateToChatWithQuery: (String) -> Unit,
    firestoreRepository: FirestoreRepository = remember { FirestoreRepository() },
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }
) {
    var crop by remember { mutableStateOf<Crop?>(null) }
    var problems by remember { mutableStateOf<List<AgriculturalProblem>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var isFavorite by remember { mutableStateOf(false) }
    var isMyCrop by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    LaunchedEffect(cropId) {
        val cropRes = firestoreRepository.getCropById(cropId)
        if (cropRes.isSuccess) {
            crop = cropRes.getOrNull()
            if (crop != null) {
                isFavorite = userServicesRepository.isFavorite(cropId)
                isMyCrop = userServicesRepository.isMyCrop(cropId)
                
                val problemsRes = firestoreRepository.getProblemsForCrop(cropId)
                if (problemsRes.isSuccess) {
                    problems = problemsRes.getOrNull() ?: emptyList()
                }
            }
        }
        isLoading = false
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text(crop?.name ?: "تفاصيل المحصول", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    },
                    actions = {
                        if (crop != null) {
                            IconButton(onClick = {
                                scope.launch {
                                    if (isFavorite) {
                                        if (userServicesRepository.removeFavorite(cropId).isSuccess) {
                                            isFavorite = false
                                            Toast.makeText(context, "تمت الإزالة من المفضلة", Toast.LENGTH_SHORT).show()
                                        }
                                    } else {
                                        if (userServicesRepository.addFavorite(cropId, "crop").isSuccess) {
                                            isFavorite = true
                                            Toast.makeText(context, "تمت الإضافة للمفضلة", Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                }
                            }) {
                                Icon(
                                    if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                                    contentDescription = "المفضلة",
                                    tint = if (isFavorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                                )
                            }
                        }
                    }
                )
            },
            floatingActionButton = {
                if (crop != null) {
                    ExtendedFloatingActionButton(
                        onClick = { onNavigateToChatWithQuery("أريد معلومات عن محصول ${crop?.name}") },
                        icon = { Icon(Icons.Outlined.SmartToy, contentDescription = null) },
                        text = { Text("اسأل المساعد") },
                        containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                        contentColor = MaterialTheme.colorScheme.onTertiaryContainer
                    )
                }
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.padding(paddingValues))
            } else if (crop == null) {
                Box(modifier = Modifier.fillMaxSize().padding(paddingValues), contentAlignment = Alignment.Center) {
                    Text("المحصول غير موجود أو تم حذفه")
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    item {
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                if ((crop?.description?.isNotEmpty() == true)) DetailSection("الوصف", crop?.description ?: "")
                                if ((crop?.plantingSeason?.isNotEmpty() == true)) DetailSection("موسم الزراعة", crop?.plantingSeason ?: "")
                                if ((crop?.soil?.isNotEmpty() == true)) DetailSection("التربة المناسبة", crop?.soil ?: "")
                                if ((crop?.irrigation?.isNotEmpty() == true)) DetailSection("إرشادات الري", crop?.irrigation ?: "")
                                if ((crop?.fertilization?.isNotEmpty() == true)) DetailSection("إرشادات التسميد", crop?.fertilization ?: "")
                                if ((crop?.notes?.isNotEmpty() == true)) DetailSection("ملاحظات هامة", crop?.notes ?: "")
                                
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(
                                    onClick = {
                                        scope.launch {
                                            if (isMyCrop) {
                                                if (userServicesRepository.removeMyCrop(cropId).isSuccess) {
                                                    isMyCrop = false
                                                    Toast.makeText(context, "تمت الإزالة من محاصيلي", Toast.LENGTH_SHORT).show()
                                                }
                                            } else {
                                                if (userServicesRepository.addMyCrop(cropId).isSuccess) {
                                                    isMyCrop = true
                                                    Toast.makeText(context, "تمت الإضافة لمحاصيلي", Toast.LENGTH_SHORT).show()
                                                }
                                            }
                                        }
                                    },
                                    modifier = Modifier.fillMaxWidth().height(50.dp),
                                    shape = RoundedCornerShape(12.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = if (isMyCrop) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.primary)
                                ) {
                                    Icon(if (isMyCrop) Icons.Filled.Check else Icons.Filled.Add, contentDescription = null)
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(if (isMyCrop) "مضاف إلى محاصيلي" else "أضف إلى محاصيلي", style = MaterialTheme.typography.titleMedium)
                                }
                            }
                        }
                    }

                    if (problems.isNotEmpty()) {
                        item {
                            Text(
                                "مشاكل هذا المحصول",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.padding(vertical = 8.dp)
                            )
                        }
                        
                        items(problems.size) { index ->
                            val problem = problems[index]
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                onClick = { onNavigateToProblem(problem.id) },
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(problem.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onErrorContainer)
                                    Text(problem.type, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))
                                }
                            }
                        }
                        
                        item {
                            Spacer(modifier = Modifier.height(64.dp))
                        }
                    }
                }
            }
        }
    }
}
