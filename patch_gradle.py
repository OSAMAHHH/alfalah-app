with open("app/build.gradle.kts", "r") as f:
    content = f.read()

deps = """    implementation(libs.androidx.credentials)
    implementation(libs.androidx.credentials.play.services)
    implementation(libs.googleid)
    implementation(libs.coil.compose)

    // Moshi & Retrofit
    implementation(libs.moshi.kotlin)
    ksp(libs.moshi.kotlin.codegen)
    implementation(libs.retrofit)
    implementation(libs.converter.moshi)
    implementation(libs.logging.interceptor)

    // Firebase Storage
    implementation("com.google.firebase:firebase-storage")
"""

content = content.replace("""    implementation(libs.androidx.credentials)
    implementation(libs.androidx.credentials.play.services)
    implementation(libs.googleid)
    implementation(libs.coil.compose)""", deps)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
