import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

deps_to_add = """
    // Moshi & Retrofit
    implementation(libs.moshi.kotlin)
    ksp(libs.moshi.kotlin.codegen)
    implementation(libs.retrofit)
    implementation(libs.converter.moshi)
    implementation(libs.logging.interceptor)

    // Firebase Storage
    implementation("com.google.firebase:firebase-storage")
"""

# Insert before closing brace of dependencies block
content = re.sub(r'(dependencies\s*\{[^}]+)(\})', r'\1' + deps_to_add + r'\2', content)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
