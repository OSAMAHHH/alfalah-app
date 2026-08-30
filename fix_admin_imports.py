import re

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "r") as f:
    text = f.read()

# Remove duplicate imports
lines = text.split('\n')
unique_lines = []
imports = set()

for line in lines:
    if line.startswith('import '):
        if line not in imports:
            imports.add(line)
            unique_lines.append(line)
    else:
        unique_lines.append(line)

text = '\n'.join(unique_lines)

# Also add @OptIn for DropdownMenu
opt_in = '@OptIn(ExperimentalMaterial3Api::class)\n@Composable'
text = re.sub(r'@Composable\s*fun ProductDialog', opt_in + '\nfun ProductDialog', text)
text = re.sub(r'@Composable\s*fun ProblemDialog', opt_in + '\nfun ProblemDialog', text)

with open("app/src/main/java/com/example/alfalah/ui/screens/admin/AdminDashboardScreen.kt", "w") as f:
    f.write(text)
