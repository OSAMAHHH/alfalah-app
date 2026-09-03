import re

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports_to_add = """import androidx.compose.ui.res.painterResource
import androidx.compose.foundation.Image
import com.example.alfalah.R
"""

content = content.replace("import androidx.compose.ui.Modifier", imports_to_add + "import androidx.compose.ui.Modifier")

# Replace text with row + image
old_text = 'Text("الدفع يدوياً عبر تطبيق جيب", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)'
new_text = """Row(verticalAlignment = Alignment.CenterVertically) {
                            Image(
                                painter = painterResource(id = R.drawable.jeeb_logo),
                                contentDescription = "شعار جيب",
                                modifier = Modifier.size(32.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("الدفع يدوياً عبر تطبيق جيب", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        }"""

content = content.replace(old_text, new_text)

with open("app/src/main/java/com/example/alfalah/ui/screens/store/CheckoutScreen.kt", "w") as f:
    f.write(content)
