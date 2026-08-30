const { initializeApp } = require('firebase/app');
const { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } = require('firebase/auth');
const { getFirestore, doc, setDoc, getDoc } = require('firebase/firestore');

const firebaseConfig = {
  apiKey: "AIzaSyBKCAQCN_kmn4K8V2puqASWKsVMHU76i00",
  projectId: "alfalah-90856"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

async function run() {
    try {
        let cred;
        try {
            cred = await createUserWithEmailAndPassword(auth, "superadmin@alfalah.com", "admin123456");
            console.log("Created new user:", cred.user.uid);
        } catch (e) {
            cred = await signInWithEmailAndPassword(auth, "superadmin@alfalah.com", "admin123456");
            console.log("Logged in existing user:", cred.user.uid);
        }
        
        // Try to make myself admin
        await setDoc(doc(db, "users", cred.user.uid), {
            id: cred.user.uid,
            role: "admin",
            name: "Super Admin",
            email: "superadmin@alfalah.com"
        });
        console.log("Made admin successfully!");
        
        // Try to write a test crop
        await setDoc(doc(db, "crops", "test_crop_admin"), {
            name: "Admin Test Crop",
            isActive: true
        });
        console.log("Wrote test crop successfully!");
        process.exit(0);
    } catch (e) {
        console.error("Error:", e);
        process.exit(1);
    }
}
run();
