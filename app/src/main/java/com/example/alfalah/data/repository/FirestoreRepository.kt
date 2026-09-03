package com.example.alfalah.data.repository

import android.net.Uri
import com.example.alfalah.data.model.*
import com.google.firebase.firestore.DocumentSnapshot
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await
import java.util.UUID

class FirestoreRepository {
    private val firestore = FirebaseFirestore.getInstance()

    // ---------------- Crops ----------------
    suspend fun getCrops(): Result<List<Crop>> = try {
        val snapshot = firestore.collection("crops").get().await()
        Result.success(snapshot.toObjects(Crop::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getCropById(id: String): Result<Crop?> = try {
        val doc = firestore.collection("crops").document(id).get().await()
        Result.success(doc.toObject(Crop::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun addCrop(item: Crop): Result<Unit> = try {
        firestore.collection("crops").add(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun updateCrop(item: Crop): Result<Unit> = try {
        if (item.id.isNotEmpty()) firestore.collection("crops").document(item.id).set(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun deleteCrop(id: String): Result<Unit> = try {
        firestore.collection("crops").document(id).delete().await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getCropsPaginated(limit: Int, lastDoc: DocumentSnapshot? = null): Result<Pair<List<Crop>, DocumentSnapshot?>> = try {
        var query = firestore.collection("crops").limit(limit.toLong())
        if (lastDoc != null) query = query.startAfter(lastDoc)
        val snapshot = query.get().await()
        Result.success(Pair(snapshot.toObjects(Crop::class.java), snapshot.documents.lastOrNull()))
    } catch (e: Exception) { Result.failure(e) }

    // ---------------- Problems ----------------
    suspend fun getProblems(): Result<List<AgriculturalProblem>> = try {
        val snapshot = firestore.collection("problems").get().await()
        Result.success(snapshot.toObjects(AgriculturalProblem::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getProblemById(id: String): Result<AgriculturalProblem?> = try {
        val doc = firestore.collection("problems").document(id).get().await()
        Result.success(doc.toObject(AgriculturalProblem::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getProblemsForCrop(cropId: String): Result<List<AgriculturalProblem>> = try {
        val snapshot = firestore.collection("problems").whereEqualTo("cropId", cropId).get().await()
        Result.success(snapshot.toObjects(AgriculturalProblem::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun addProblem(item: AgriculturalProblem): Result<Unit> = try {
        firestore.collection("problems").add(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun updateProblem(item: AgriculturalProblem): Result<Unit> = try {
        if (item.id.isNotEmpty()) firestore.collection("problems").document(item.id).set(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun deleteProblem(id: String): Result<Unit> = try {
        firestore.collection("problems").document(id).delete().await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getProblemsPaginated(limit: Int, lastDoc: DocumentSnapshot? = null): Result<Pair<List<AgriculturalProblem>, DocumentSnapshot?>> = try {
        var query = firestore.collection("problems").limit(limit.toLong())
        if (lastDoc != null) query = query.startAfter(lastDoc)
        val snapshot = query.get().await()
        Result.success(Pair(snapshot.toObjects(AgriculturalProblem::class.java), snapshot.documents.lastOrNull()))
    } catch (e: Exception) { Result.failure(e) }

    // ---------------- Products ----------------
    suspend fun getProducts(): Result<List<Product>> = try {
        val snapshot = firestore.collection("products").get().await()
        Result.success(snapshot.toObjects(Product::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getProductById(id: String): Result<Product?> = try {
        val doc = firestore.collection("products").document(id).get().await()
        Result.success(doc.toObject(Product::class.java))
    } catch (e: Exception) { Result.failure(e) }

    suspend fun getProductsByIds(ids: List<String>): Result<List<Product>> = try {
        if (ids.isEmpty()) Result.success(emptyList())
        else {
            val snapshot = firestore.collection("products").whereIn("id", ids).get().await()
            Result.success(snapshot.toObjects(Product::class.java))
        }
    } catch (e: Exception) { Result.failure(e) }

    suspend fun addProduct(item: Product): Result<Unit> = try {
        firestore.collection("products").add(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun updateProduct(item: Product): Result<Unit> = try {
        if (item.id.isNotEmpty()) firestore.collection("products").document(item.id).set(item).await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun deleteProduct(id: String): Result<Unit> = try {
        firestore.collection("products").document(id).delete().await()
        Result.success(Unit)
    } catch (e: Exception) { Result.failure(e) }

    suspend fun uploadImage(uri: Uri): Result<String> = try {
        val storage = FirebaseStorage.getInstance()
        val ref = storage.reference.child("images/${UUID.randomUUID()}")
        ref.putFile(uri).await()
        Result.success(ref.downloadUrl.await().toString())
    } catch (e: Exception) { Result.failure(e) }
}
