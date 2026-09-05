import re

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val uid = getUserId() ?: return Result.failure(Exception("Not logged in"))',
    'val uid = getUserId() ?: run { android.util.Log.e("UserServicesRepository", "addToCart failed: Not logged in"); return Result.failure(Exception("Not logged in")) }'
)

content = content.replace(
    '''            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }''',
    '''            Result.success(Unit)
        } catch (e: Exception) {
            android.util.Log.e("UserServicesRepository", "addToCart failed: ${e.message}", e)
            Result.failure(e)
        }'''
)

with open("app/src/main/java/com/example/alfalah/data/repository/UserServicesRepository.kt", "w") as f:
    f.write(content)
