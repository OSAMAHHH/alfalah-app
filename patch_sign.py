with open("app/build.gradle.kts", "r") as f:
    content = f.read()

bad = """    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }"""

good = """    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("debug")
        }
    }"""

content = content.replace(bad, good)
with open("app/build.gradle.kts", "w") as f:
    f.write(content)
