package com.example.alfalah.data.repository

import com.example.alfalah.data.model.User
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class AuthRepository {
    private val auth = FirebaseAuth.getInstance()
    private val firestore = FirebaseFirestore.getInstance()

    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()

    init {
        auth.addAuthStateListener { firebaseAuth ->
            val user = firebaseAuth.currentUser
            if (user != null) {
                fetchUserFromFirestore(user.uid)
            } else {
                _currentUser.value = null
            }
        }
    }

    private fun fetchUserFromFirestore(uid: String) {
        firestore.collection("users").document(uid).get()
            .addOnSuccessListener { document ->
                if (document.exists()) {
                    _currentUser.value = document.toObject(User::class.java)
                }
            }
    }

    suspend fun login(email: String, password: String): Result<Unit> {
        return try {
            auth.signInWithEmailAndPassword(email, password).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun register(name: String, email: String, password: String): Result<Unit> {
        return try {
            val result = auth.createUserWithEmailAndPassword(email, password).await()
            val user = User(id = result.user!!.uid, name = name, email = email, role = "user")
            firestore.collection("users").document(user.id).set(user).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    
    suspend fun googleSignIn(idToken: String): Result<Unit> {
        return try {
            val credential = GoogleAuthProvider.getCredential(idToken, null)
            val result = auth.signInWithCredential(credential).await()
            val user = result.user!!
            // Check if user exists in Firestore
            val doc = firestore.collection("users").document(user.uid).get().await()
            if (!doc.exists()) {
                val newUser = User(id = user.uid, name = user.displayName ?: "مزارع", email = user.email ?: "", role = "user")
                firestore.collection("users").document(user.uid).set(newUser).await()
            }
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }


    suspend fun updateUserName(newName: String): Result<Unit> {
        val user = auth.currentUser ?: return Result.failure(Exception("غير مسجل الدخول"))
        return try {
            firestore.collection("users").document(user.uid)
                .update("name", newName).await()
            
            // Update local state directly to reflect immediately
            _currentUser.value = _currentUser.value?.copy(name = newName)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun logout() {
        auth.signOut()
    }
}
