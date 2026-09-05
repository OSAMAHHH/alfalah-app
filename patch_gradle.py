with open("app/build.gradle.kts", "r") as f:
    content = f.read()

deps_str = "dependencies {"
new_deps_str = 'dependencies {\n    implementation("com.google.android.gms:play-services-location:21.3.0")'

if "play-services-location" not in content:
    content = content.replace(deps_str, new_deps_str)
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
