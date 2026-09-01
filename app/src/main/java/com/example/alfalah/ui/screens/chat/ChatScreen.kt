package com.example.alfalah.ui.screens.chat

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Send
import androidx.compose.material.icons.outlined.SmartToy
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.alfalah.data.model.Product
import com.example.alfalah.ui.components.EmptyState

fun parseMarkdownText(markdown: String): AnnotatedString {
    val lines = markdown.lines()
    val processedLines = lines.map { line ->
        var trimmed = line.trimStart()
        if (trimmed.startsWith("### ") || trimmed.startsWith("## ") || trimmed.startsWith("# ")) {
            trimmed = "**" + trimmed.replaceFirst(Regex("^#+\\s*"), "") + "**"
        } else if (trimmed.startsWith("* ") || trimmed.startsWith("- ")) {
            trimmed = "• " + trimmed.substring(2)
        }
        trimmed
    }
    val processedText = processedLines.joinToString("\n")

    return buildAnnotatedString {
        val regex = Regex("\\*\\*(.*?)\\*\\*")
        var currentIndex = 0

        regex.findAll(processedText).forEach { matchResult ->
            val start = matchResult.range.first
            val end = matchResult.range.last + 1
            val boldContent = matchResult.groupValues[1]

            if (start > currentIndex) {
                append(processedText.substring(currentIndex, start))
            }

            withStyle(SpanStyle(fontWeight = FontWeight.Bold)) {
                append(boldContent)
            }

            currentIndex = end
        }

        if (currentIndex < processedText.length) {
            append(processedText.substring(currentIndex))
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    onBack: () -> Unit,
    onNavigateToProduct: (String) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: ChatViewModel = viewModel()
) {
    val messages by viewModel.messages.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    LaunchedEffect(messages.size, isLoading) {
        if (messages.isNotEmpty()) listState.animateScrollToItem(messages.size)
    }

    Scaffold(
        topBar = {
            Surface(shadowElevation = 4.dp, color = MaterialTheme.colorScheme.surface) {
                TopAppBar(
                    title = { 
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(modifier = Modifier.size(40.dp).background(MaterialTheme.colorScheme.primaryContainer, CircleShape), contentAlignment = Alignment.Center) {
                                Icon(Icons.Outlined.SmartToy, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text("المساعد الزراعي", style = MaterialTheme.typography.titleMedium)
                                Text("متصل دائماً للإجابة على استفساراتك", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                            }
                        }
                    },
                    navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "رجوع") } },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent)
                )
            }
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Column(modifier = modifier.fillMaxSize().padding(padding)) {
            if (messages.isEmpty()) {
                Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        EmptyState(
                            icon = Icons.Outlined.SmartToy,
                            title = "كيف أساعدك اليوم؟",
                            message = "أنا هنا لمساعدتك في تشخيص أمراض النباتات، اقتراح الأسمدة، والإجابة عن أي استفسار زراعي."
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        val suggestions = listOf("ما هو أفضل سماد للطماطم؟", "كيف أعالج اصفرار أوراق الليمون؟", "متى أزرع القمح؟")
                        suggestions.forEach { text ->
                            Surface(
                                modifier = Modifier.padding(vertical = 4.dp).clickable { viewModel.sendMessage(text) },
                                shape = RoundedCornerShape(16.dp),
                                color = MaterialTheme.colorScheme.surfaceVariant,
                                border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.5f))
                            ) {
                                Text(text, modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            } else {
                LazyColumn(state = listState, modifier = Modifier.weight(1f), contentPadding = PaddingValues(24.dp), verticalArrangement = Arrangement.spacedBy(24.dp)) {
                    items(messages) { message -> ChatMessageBubble(message = message, onNavigateToProduct = onNavigateToProduct) }
                    if (isLoading) item { TypingIndicator() }
                }
            }

            Surface(color = MaterialTheme.colorScheme.surface, shadowElevation = 16.dp) {
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp).navigationBarsPadding(), verticalAlignment = Alignment.CenterVertically) {
                    OutlinedTextField(
                        value = inputText, onValueChange = { inputText = it },
                        modifier = Modifier.weight(1f), placeholder = { Text("اكتب سؤالك الزراعي...") },
                        shape = RoundedCornerShape(24.dp), maxLines = 4,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = MaterialTheme.colorScheme.primary, unfocusedBorderColor = MaterialTheme.colorScheme.outline,
                            focusedContainerColor = MaterialTheme.colorScheme.surface, unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha=0.3f)
                        )
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    IconButton(
                        onClick = { if (inputText.isNotBlank() && !isLoading) { viewModel.sendMessage(inputText); inputText = "" } },
                        enabled = inputText.isNotBlank() && !isLoading,
                        modifier = Modifier.size(56.dp).background(if (inputText.isNotBlank() && !isLoading) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        Icon(Icons.AutoMirrored.Outlined.Send, contentDescription = "إرسال", tint = if (inputText.isNotBlank() && !isLoading) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
fun ChatMessageBubble(message: ChatMessageUi, onNavigateToProduct: (String) -> Unit) {
    val isUser = message.isUser
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start, verticalAlignment = Alignment.Bottom) {
        if (!isUser) {
            Box(modifier = Modifier.size(36.dp).background(MaterialTheme.colorScheme.primaryContainer, CircleShape), contentAlignment = Alignment.Center) {
                Icon(Icons.Outlined.SmartToy, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
            }
            Spacer(modifier = Modifier.width(12.dp))
        }

        Surface(
            color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
            shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp, bottomStart = if (isUser) 24.dp else 4.dp, bottomEnd = if (isUser) 4.dp else 24.dp),
            modifier = Modifier.widthIn(max = 300.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = parseMarkdownText(message.text),
                    style = MaterialTheme.typography.bodyLarge,
                    color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                    lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.5f
                )
                if (message.recommendedProducts.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("منتجات متوفرة في المتجر للعلاج:", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    Spacer(modifier = Modifier.height(12.dp))
                    message.recommendedProducts.forEach { product ->
                        Surface(
                            onClick = { onNavigateToProduct(product.id) },
                            color = MaterialTheme.colorScheme.surface, shape = RoundedCornerShape(12.dp), shadowElevation = 2.dp,
                            modifier = Modifier.padding(bottom = 8.dp)
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                                Column {
                                    Text(product.name, style = MaterialTheme.typography.titleSmall, color = MaterialTheme.colorScheme.onSurface)
                                    Text("${product.price} ر.ي", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
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
fun TypingIndicator() {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Start, verticalAlignment = Alignment.Bottom) {
        Box(modifier = Modifier.size(36.dp).background(MaterialTheme.colorScheme.primaryContainer, CircleShape), contentAlignment = Alignment.Center) {
            Icon(Icons.Outlined.SmartToy, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(12.dp))
        Surface(color = MaterialTheme.colorScheme.surfaceVariant, shape = RoundedCornerShape(24.dp, 24.dp, 24.dp, 4.dp)) {
            Row(modifier = Modifier.padding(horizontal = 20.dp, vertical = 20.dp), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                Dot(delay = 0); Dot(delay = 150); Dot(delay = 300)
            }
        }
    }
}

@Composable
fun Dot(delay: Int) {
    val transition = rememberInfiniteTransition()
    val alpha by transition.animateFloat(initialValue = 0.3f, targetValue = 1f, animationSpec = infiniteRepeatable(animation = tween(durationMillis = 600, delayMillis = delay, easing = LinearEasing), repeatMode = RepeatMode.Reverse))
    Box(modifier = Modifier.size(8.dp).background(MaterialTheme.colorScheme.primary.copy(alpha = alpha), CircleShape))
}

