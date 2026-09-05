package com.example.alfalah.ui.screens.chat

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Chat
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.example.alfalah.data.model.Conversation
import com.example.alfalah.data.repository.UserServicesRepository
import com.example.alfalah.ui.components.EmptyState
import com.example.alfalah.ui.components.LoadingState
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ConversationsScreen(
    onBack: () -> Unit,
    onNavigateToChat: (String) -> Unit,
    userServicesRepository: UserServicesRepository = remember { UserServicesRepository() }
) {
    var conversations by remember { mutableStateOf<List<Conversation>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    
    val currentUser = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
    if (currentUser == null) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("المساعد الزراعي", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier.fillMaxSize().padding(padding).padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(Icons.Filled.Chat, contentDescription = null, modifier = Modifier.size(72.dp), tint = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(16.dp))
                Text("يرجى تسجيل الدخول أولاً", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
                Spacer(modifier = Modifier.height(8.dp))
                Text("تحتاج إلى تسجيل الدخول لاستخدام المساعد الزراعي الذكي.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        return
    }
    val scope = rememberCoroutineScope()
    val dateFormat = remember { SimpleDateFormat("yyyy/MM/dd HH:mm", Locale("ar")) }

    fun loadConversations() {
        scope.launch {
            isLoading = true
            conversations = userServicesRepository.getConversations()
            isLoading = false
        }
    }

    LaunchedEffect(Unit) {
        loadConversations()
    }

    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("المحادثات السابقة", fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع")
                        }
                    }
                )
            },
            floatingActionButton = {
                FloatingActionButton(onClick = { onNavigateToChat("") }) {
                    Icon(Icons.Filled.Add, contentDescription = "محادثة جديدة")
                }
            }
        ) { paddingValues ->
            if (isLoading) {
                LoadingState(modifier = Modifier.padding(paddingValues))
            } else if (conversations.isEmpty()) {
                EmptyState(
                    icon = Icons.Filled.Chat,
                    title = "لا توجد محادثات",
                    message = "ابدأ محادثة جديدة مع المساعد الزراعي",
                    modifier = Modifier.padding(paddingValues)
                )
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(conversations.size) { index ->
                        val conv = conversations[index]
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            onClick = { onNavigateToChat(conv.id) },
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = conv.title.ifEmpty { "محادثة زراعية" },
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.Bold,
                                        maxLines = 1
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = dateFormat.format(Date(conv.updatedAt)),
                                        style = MaterialTheme.typography.labelMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                                IconButton(onClick = {
                                    scope.launch {
                                        userServicesRepository.deleteConversation(conv.id)
                                        loadConversations()
                                    }
                                }) {
                                    Icon(Icons.Filled.Delete, contentDescription = "حذف", tint = MaterialTheme.colorScheme.error)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
