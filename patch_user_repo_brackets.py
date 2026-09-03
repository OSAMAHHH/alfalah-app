with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "}" and "suspend fun uploadImage" in "".join(lines[i:]):
        continue
    new_lines.append(line)

if new_lines[-1].strip() != "}":
    new_lines.append("\n}\n")

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.writelines(new_lines)
