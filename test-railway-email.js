async function testRailway() {
  const apiKey = 'AIzaSyBKCAQCN_kmn4K8V2puqASWKsVMHU76i00';
  const email = `testuser_${Date.now()}@example.com`;
  const password = "password123";
  
  console.log(`1. Signing up with email ${email}...`);
  const authRes = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, returnSecureToken: true })
  });
  const authData = await authRes.json();
  
  if (!authData.idToken) {
    console.error("Failed to get ID token", authData);
    return;
  }
  
  const token = authData.idToken;
  console.log("Got token...");
  
  console.log("2. Sending request to Railway backend...");
  const res = await fetch('https://alfalah-app-production.up.railway.app/api/ai/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message: "ما هي مشاكل الطماطم؟" })
  });
  
  const status = res.status;
  const text = await res.text();
  console.log(`\nRAILWAY HTTP STATUS: ${status}`);
  console.log(`RAILWAY RESPONSE BODY: ${text}`);
}
testRailway();
