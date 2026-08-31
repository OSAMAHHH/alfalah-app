import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = "AIzaSyBKCAQCN_kmn4K8V2puqASWKsVMHU76i00"
BASE_URL = "https://firestore.googleapis.com/v1/projects/alfalah-90856/databases/(default)/documents"

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
payload = {"email": "temp_admin_test_6@example.com", "password": "password123", "returnSecureToken": True}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(req, context=ctx) as response:
    res = json.loads(response.read().decode())
    token = res["idToken"]
    uid = res["localId"]
    print("UID:", uid)

url = f"{BASE_URL}/users?documentId={uid}"
payload = {"fields": {"role": {"stringValue": "admin"}}}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization', f'Bearer {token}')
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print("Success!", response.read().decode())
except urllib.error.HTTPError as e:
    print("Failed!", e.read().decode())
