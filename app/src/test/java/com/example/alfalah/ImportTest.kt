package com.example.alfalah

import androidx.test.ext.junit.runners.AndroidJUnit4
import com.google.firebase.FirebaseApp
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.tasks.await
import org.json.JSONObject
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import java.io.File
import androidx.test.core.app.ApplicationProvider
import android.content.Context

@RunWith(RobolectricTestRunner::class)
@Config(manifest=Config.NONE)
class ImportTest {

    @Test
    fun doImport() = runBlocking {
        val context = ApplicationProvider.getApplicationContext<Context>()
        FirebaseApp.initializeApp(context)
        val db = FirebaseFirestore.getInstance()
        
        val jsonStr = File("../scripts/batch_2_verified.json").readText()
        val parsedJson = JSONObject(jsonStr)
        val problems = parsedJson.getJSONArray("agricultural_problems")
        
        val batch = db.batch()
        for (i in 0 until problems.length()) {
            val probJson = problems.getJSONObject(i)
            val id = probJson.getString("id")
            val map = mutableMapOf<String, Any>()
            val keys = probJson.keys()
            while (keys.hasNext()) {
                val key = keys.next()
                if (!key.startsWith("_") && key != "id") {
                    val value = probJson.get(key)
                    if (value is org.json.JSONArray) {
                        val list = mutableListOf<String>()
                        for (j in 0 until value.length()) {
                            list.add(value.getString(j))
                        }
                        map[key] = list
                    } else {
                        map[key] = value
                    }
                }
            }
            batch.set(db.collection("agricultural_problems").document(id), map)
        }
        batch.commit().await()
        
        val snap = db.collection("agricultural_problems").get().await()
        println("IMPORTED DOCS: ${snap.size()}")
    }
}
