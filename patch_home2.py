import re

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

imports = """
import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationServices
"""
content = content.replace("import kotlinx.coroutines.launch\n", "import kotlinx.coroutines.launch\n" + imports)

# Find the LaunchedEffect(Unit) block and replace it
# The original block:
#     LaunchedEffect(Unit) { 
#         weather = weatherRepository.getCurrentWeather().getOrNull() 
#     }

new_effect = """
    val context = LocalContext.current
    val fusedLocationClient = remember { LocationServices.getFusedLocationProviderClient(context) }
    var locationError by remember { mutableStateOf<String?>(null) }
    
    val locationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
            }
        } else {
            locationError = "تم رفض إذن الموقع. نعرض لك طقس غير دقيق."
            scope.launch {
                weather = weatherRepository.getCurrentWeather(24.7136, 46.6753).getOrNull()
            }
        }
    }

    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            try {
                fusedLocationClient.lastLocation.addOnSuccessListener { location ->
                    if (location != null) {
                        scope.launch {
                            weather = weatherRepository.getCurrentWeather(location.latitude, location.longitude).getOrNull()
                        }
                    } else {
                        locationError = "تعذر تحديد الموقع الجغرافي."
                    }
                }
            } catch(e: SecurityException) {
                locationError = "تم رفض إذن الموقع."
            }
        } else {
            locationPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }
"""

content = re.sub(r'LaunchedEffect\(Unit\)\s*\{\s*weather = weatherRepository\.getCurrentWeather\(\)\.getOrNull\(\)\s*\}', new_effect, content)

# Show error if permission denied
weather_error_display = """
            if (locationError != null && weather == null) {
                Text(
                    text = locationError!!,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(horizontal = 24.dp)
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
"""
# Insert right before 'ElevatedCard(' representing the Weather card.
content = content.replace("ElevatedCard(", weather_error_display + "            ElevatedCard(", 1)

with open("app/src/main/java/com/example/alfalah/ui/screens/home/HomeScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
