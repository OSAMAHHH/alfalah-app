import re
with open("app/src/main/java/com/example/alfalah/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()

# I will replace `val user = result.user` with `val firebaseUser = result.user ?: return Result.failure(Exception("Login failed: no user data"))`
content = content.replace("val user = result.user\n", 'val firebaseUser = result.user ?: return Result.failure(Exception("Login failed: no user data"))\n')
content = content.replace("result.user.uid", "firebaseUser.uid")
content = content.replace("result.user.displayName", "firebaseUser.displayName")
content = content.replace("result.user.email", "firebaseUser.email")
# Wait, earlier I replaced `result.user!!` with `result.user`. The line was `val user = result.user!!`
# Let's just fix it by replacing all `result.user?.uid` or similar back if any, and replacing `user.uid` with `user?.uid`.
# A safer way is to just write a good python script using exact replacements.
