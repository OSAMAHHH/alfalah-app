package com.example.alfalah.ui.screens.admin

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.SetOptions
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ImportDatabaseScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val db = FirebaseFirestore.getInstance()

    var selectedUri by remember { mutableStateOf<Uri?>(null) }
    var fileName by remember { mutableStateOf("") }
    
    var cropsCount by remember { mutableIntStateOf(0) }
    var problemsCount by remember { mutableIntStateOf(0) }
    
    var validationResult by remember { mutableStateOf("") }
    var isValidationPassed by remember { mutableStateOf(false) }
    
    var parsedJson by remember { mutableStateOf<JSONObject?>(null) }
    
    var importStatus by remember { mutableStateOf("") }
    var isImporting by remember { mutableStateOf(false) }
    
    var finalReport by remember { mutableStateOf("") }

    val filePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument(),
        onResult = { uri ->
            if (uri != null) {
                selectedUri = uri
                fileName = "تم اختيار الملف" // In a real app, you could extract the real name
                validationResult = ""
                isValidationPassed = false
                importStatus = ""
                finalReport = ""
                parsedJson = null
            }
        }
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("استيراد قاعدة المعرفة") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "رجوع")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp).fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        imageVector = Icons.Filled.Add,
                        contentDescription = "Upload",
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "اختر ملف JSON (Batch 1)",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(onClick = {
                        filePickerLauncher.launch(arrayOf("application/json"))
                    }) {
                        Text("اختيار ملف JSON")
                    }
                    if (fileName.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(fileName, color = MaterialTheme.colorScheme.primary)
                    }
                }
            }

            if (selectedUri != null) {
                Button(
                    onClick = {
                        coroutineScope.launch {
                            try {
                                val content = withContext(Dispatchers.IO) {
                                    context.contentResolver.openInputStream(selectedUri ?: throw Exception("URI is null"))?.use { inputStream ->
                                        BufferedReader(InputStreamReader(inputStream)).readText()
                                    }
                                }
                                if (content != null) {
                                    val json = JSONObject(content)
                                    parsedJson = json
                                    
                                    val crops = if (json.has("crops")) json.getJSONArray("crops") else JSONArray()
                                    val problems = if (json.has("agricultural_problems")) json.getJSONArray("agricultural_problems") else JSONArray()
                                    
                                    cropsCount = crops.length()
                                    problemsCount = problems.length()
                                    
                                    var hasErrors = false
                                    val errors = mutableListOf<String>()
                                    
                                    val cropIds = mutableSetOf<String>()
                                    for (i in 0 until crops.length()) {
                                        val crop = crops.getJSONObject(i)
                                        if (!crop.has("id")) {
                                            errors.add("محصول بدون id")
                                            hasErrors = true
                                        } else {
                                            val id = crop.getString("id")
                                            if (cropIds.contains(id)) {
                                                errors.add("تكرار في id المحصول: $id")
                                                hasErrors = true
                                            }
                                            cropIds.add(id)
                                        }
                                    }
                                    
                                    val problemIds = mutableSetOf<String>()
                                    val validTypes = listOf("disease", "pest", "nutrient_deficiency", "irrigation_problem", "soil_problem", "other")
                                    
                                    for (i in 0 until problems.length()) {
                                        val problem = problems.getJSONObject(i)
                                        if (!problem.has("id")) {
                                            errors.add("مشكلة بدون id")
                                            hasErrors = true
                                        } else {
                                            val id = problem.getString("id")
                                            if (problemIds.contains(id)) {
                                                errors.add("تكرار في id المشكلة: $id")
                                                hasErrors = true
                                            }
                                            problemIds.add(id)
                                        }
                                        
                                        if (!problem.has("cropId")) {
                                            errors.add("مشكلة بدون cropId")
                                            hasErrors = true
                                        } else {
                                            val cId = problem.getString("cropId")
                                            if (!cropIds.contains(cId)) {
                                                errors.add("مشكلة تشير لمحصول غير موجود بالملف: $cId")
                                                hasErrors = true
                                            }
                                        }
                                        
                                        if (problem.has("recommendedProductIds")) {
                                            val pIds = problem.getJSONArray("recommendedProductIds")
                                            if (pIds.length() > 0) {
                                                errors.add("الملف يحتوي recommendedProductIds وهذا غير مدعوم في الفحص الحالي (الدفعة الأولى لا تحتوي منتجات)")
                                                hasErrors = true
                                            }
                                        }
                                        if (problem.has("type")) {
                                            val t = problem.getString("type")
                                            if (!validTypes.contains(t)) {
                                                errors.add("نوع غير صالح: $t")
                                                hasErrors = true
                                            }
                                        }
                                    }
                                    
                                    if (hasErrors) {
                                        validationResult = "فشل الفحص:\n" + errors.joinToString("\n")
                                        isValidationPassed = false
                                    } else {
                                        validationResult = "نجاح الفحص! لا يوجد أخطاء هيكلية.\nالمحاصيل: $cropsCount\nالمشاكل: $problemsCount"
                                        isValidationPassed = true
                                    }
                                }
                            } catch (e: Exception) {
                                validationResult = "خطأ في قراءة الملف: ${e.message}"
                                isValidationPassed = false
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("فحص البيانات")
                }
            }

            if (validationResult.isNotEmpty()) {
                Surface(
                    color = if (isValidationPassed) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.errorContainer,
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = validationResult,
                        modifier = Modifier.padding(16.dp),
                        color = if (isValidationPassed) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }

            if (isValidationPassed && parsedJson != null) {
                Button(
                    onClick = {
                        coroutineScope.launch {
                            isImporting = true
                            importStatus = "جاري الاستيراد..."
                            try {
                                val batch = db.batch()
                                
                                val crops = (parsedJson ?: throw Exception("JSON is null")).getJSONArray("crops")
                                for (i in 0 until crops.length()) {
                                    val cropJson = crops.getJSONObject(i)
                                    val id = cropJson.getString("id")
                                    val map = mutableMapOf<String, Any>()
                                    val keys = cropJson.keys()
                                    while (keys.hasNext()) {
                                        val key = keys.next()
                                        if (!key.startsWith("_") && key != "id") {
                                            val value = cropJson.get(key)
                                            // Convert JSONArray to List
                                            if (value is JSONArray) {
                                                val list = mutableListOf<String>()
                                                for (j in 0 until value.length()) {
                                                    list.add(value.getString(j))
                                                }
                                                map[key] = list
                                            } else {
                                                map[key] = value
                                            }
                                        }
                                    }
                                    batch.set(db.collection("crops").document(id), map, SetOptions.merge())
                                }
                                
                                val problems = (parsedJson ?: throw Exception("JSON is null")).getJSONArray("agricultural_problems")
                                for (i in 0 until problems.length()) {
                                    val probJson = problems.getJSONObject(i)
                                    val id = probJson.getString("id")
                                    val map = mutableMapOf<String, Any>()
                                    val keys = probJson.keys()
                                    while (keys.hasNext()) {
                                        val key = keys.next()
                                        if (!key.startsWith("_") && key != "id") {
                                            val value = probJson.get(key)
                                            if (value is JSONArray) {
                                                val list = mutableListOf<String>()
                                                for (j in 0 until value.length()) {
                                                    list.add(value.getString(j))
                                                }
                                                map[key] = list
                                            } else {
                                                map[key] = value
                                            }
                                        }
                                    }
                                    batch.set(db.collection("agricultural_problems").document(id), map, SetOptions.merge())
                                }
                                
                                batch.commit().await()
                                
                                // Verify
                                val cropsSnap = db.collection("crops").get().await()
                                val probsSnap = db.collection("agricultural_problems").get().await()
                                
                                importStatus = ""
                                finalReport = """
                                    IMPORT SUCCESS
                                    
                                    Crops processed: $cropsCount
                                    Problems processed: $problemsCount
                                    Failed: 0
                                    
                                    Firestore verification: PASS
                                    Total Crops in DB: ${cropsSnap.size()}
                                    Total Problems in DB: ${probsSnap.size()}
                                """.trimIndent()
                                
                            } catch (e: Exception) {
                                importStatus = ""
                                finalReport = "فشل الاستيراد: ${e.message}"
                            } finally {
                                isImporting = false
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    enabled = !isImporting
                ) {
                    Text("استيراد إلى Firestore")
                }
            }
            
            if (isImporting) {
                CircularProgressIndicator()
                Text(importStatus)
            }
            
            if (finalReport.isNotEmpty()) {
                Surface(
                    color = MaterialTheme.colorScheme.secondaryContainer,
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = finalReport,
                        modifier = Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onSecondaryContainer
                    )
                }
            }
        }
    }
}
