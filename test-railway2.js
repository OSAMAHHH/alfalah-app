const fs = require('fs');
async function testRailway() {
  console.log("Sending request to Railway backend without token to see if it hits 401 or 404...");
  const res = await fetch('https://alfalah-app-production.up.railway.app/api/ai/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: "hello" })
  });
  
  const status = res.status;
  const text = await res.text();
  console.log(`\nRAILWAY HTTP STATUS: ${status}`);
  console.log(`RAILWAY RESPONSE BODY: ${text}`);
}
testRailway();
