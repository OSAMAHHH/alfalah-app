package com.example.alfalah.data.repository

import com.example.alfalah.data.model.AgriculturalProblem
import com.example.alfalah.data.model.Crop
import com.example.alfalah.data.model.Product
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import android.net.Uri
import java.util.UUID
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext


class FirestoreRepository {
    private val firestore = FirebaseFirestore.getInstance()
    private val productsCollection = firestore.collection("products")
    private val cropsCollection = firestore.collection("crops")
    private val problemsCollection = firestore.collection("agricultural_problems")

    
    suspend fun uploadImage(uri: Uri): Result<String> = withContext(Dispatchers.IO) {
        try {
            val storageRef = FirebaseStorage.getInstance().reference.child("products/${UUID.randomUUID()}.jpg")
            storageRef.putFile(uri).await()
            val downloadUrl = storageRef.downloadUrl.await().toString()
            Result.success(downloadUrl)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getProducts(): Result<List<Product>> {
        return try {
            val snapshot = productsCollection.get().await()
            val products = snapshot.documents.mapNotNull { it.toObject(Product::class.java) }
            Result.success(products)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addProduct(product: Product): Result<Unit> {
        return try {
            val docRef = productsCollection.document()
            productsCollection.document(docRef.id).set(product.copy(id = docRef.id)).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateProduct(product: Product): Result<Unit> {
        return try {
            productsCollection.document(product.id).set(product).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deleteProduct(productId: String): Result<Unit> {
        return try {
            productsCollection.document(productId).delete().await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getProductById(id: String): Result<Product> {
        return try {
            val doc = productsCollection.document(id).get().await()
            val product = doc.toObject(Product::class.java)
            if (product != null) Result.success(product) else Result.failure(Exception("Not found"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // --- Crops ---
    suspend fun getCrops(): Result<List<Crop>> {
        return try {
            val snapshot = cropsCollection.get().await()
            val crops = snapshot.documents.mapNotNull { it.toObject(Crop::class.java) }
            Result.success(crops)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addCrop(crop: Crop): Result<Unit> {
        return try {
            val docRef = cropsCollection.document()
            cropsCollection.document(docRef.id).set(crop.copy(id = docRef.id)).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateCrop(crop: Crop): Result<Unit> {
        return try {
            cropsCollection.document(crop.id).set(crop).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // --- Agricultural Problems ---
    suspend fun getProblemsForCrop(cropId: String): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.whereEqualTo("cropId", cropId).get().await()
            val problems = snapshot.documents.mapNotNull { it.toObject(AgriculturalProblem::class.java) }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getProblems(): Result<List<AgriculturalProblem>> {
        return try {
            val snapshot = problemsCollection.get().await()
            val problems = snapshot.documents.mapNotNull { it.toObject(AgriculturalProblem::class.java) }
            Result.success(problems)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addProblem(problem: AgriculturalProblem): Result<Unit> {
        return try {
            val docRef = problemsCollection.document()
            problemsCollection.document(docRef.id).set(problem.copy(id = docRef.id)).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateProblem(problem: AgriculturalProblem): Result<Unit> {
        return try {
            problemsCollection.document(problem.id).set(problem).await()
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
