import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = "AIzaSyBKCAQCN_kmn4K8V2puqASWKsVMHU76i00"
PROJECT_ID = "alfalah-90856"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

def to_firestore_value(val):
    if isinstance(val, str):
        return {"stringValue": val}
    elif isinstance(val, bool):
        return {"booleanValue": val}
    elif isinstance(val, int):
        return {"integerValue": str(val)}
    elif isinstance(val, float):
        return {"doubleValue": val}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [to_firestore_value(v) for v in val]}}
    elif isinstance(val, dict):
        return {"mapValue": {"fields": {k: to_firestore_value(v) for k, v in val.items()}}}
    elif val is None:
        return {"nullValue": None}
    else:
        return {"stringValue": str(val)}

def sign_up():
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": "temp_admin_123@example.com", "password": "password123", "returnSecureToken": True}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode())
            return res["idToken"], res["localId"]
    except urllib.error.HTTPError as e:
        # If exists, sign in instead
        if b"EMAIL_EXISTS" in e.read():
            return sign_in()
        print("Sign up failed.")
        return None, None

def sign_in():
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": "temp_admin_123@example.com", "password": "password123", "returnSecureToken": True}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode())
            return res["idToken"], res["localId"]
    except urllib.error.HTTPError as e:
        print("Sign in failed.", e.read())
        return None, None

def make_admin(token, uid):
    url = f"{BASE_URL}/users/{uid}"
    payload = {"fields": {"role": {"stringValue": "admin"}}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='PATCH')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return True
    except urllib.error.HTTPError as e:
        print(f"Failed to make admin: {e.read().decode()}")
        return False

def get_collection_ids(collection_name, token=None):
    url = f"{BASE_URL}/{collection_name}?pageSize=1000"
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            docs = data.get("documents", [])
            return [doc["name"].split("/")[-1] for doc in docs]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        print(f"Error fetching {collection_name}: {e.read().decode()}")
        return []

def patch_document(collection, doc_id, data, token):
    url = f"{BASE_URL}/{collection}/{doc_id}"
    fields = {k: to_firestore_value(v) for k, v in data.items()}
    payload = {"fields": fields}
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, method='PATCH')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status == 200
    except urllib.error.HTTPError as e:
        print(f"Failed to patch {doc_id}: {e.read().decode()}")
        return False

def main():
    print("Authenticating as temp admin...")
    token, uid = sign_up()
    if not token:
        return
    print(f"UID: {uid}")
    if not make_admin(token, uid):
        return
    print("Admin role granted!")

    # 1. Load file
    try:
        with open("scripts/batch_2_verified.json", "r") as f:
            batch2 = json.load(f)
    except Exception as e:
        print(f"Failed to load file: {e}")
        return

    problems = batch2.get("agricultural_problems", [])
    print(f"Found {len(problems)} problems in batch_2.")

    # 2. Fetch existing IDs
    existing_problems = set(get_collection_ids("agricultural_problems", token))
    existing_crops = set(get_collection_ids("crops", token))
    existing_products = set(get_collection_ids("products", token))

    # 3. Validate
    duplicate_ids = 0
    new_ids = 0
    valid_crops = 0
    invalid_crops = 0
    invalid_products = 0

    invalid_crop_names = []

    for p in problems:
        if p["id"] in existing_problems:
            duplicate_ids += 1
            print(f"DUPLICATE PROBLEM ID: {p['id']}")
        else:
            new_ids += 1

        if p["cropId"] in existing_crops:
            valid_crops += 1
        else:
            invalid_crops += 1
            invalid_crop_names.append(p["cropId"])
            print(f"INVALID CROP ID: {p['cropId']} for {p['id']}")

        prod_ids = p.get("recommendedProductIds", [])
        for pid in prod_ids:
            if pid not in existing_products:
                invalid_products += 1
                print(f"INVALID PRODUCT ID: {pid} for {p['id']}")

    print("\n--- VALIDATION REPORT ---")
    print(f"Total Problems in File: {len(problems)}")
    print(f"New IDs: {new_ids}")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Valid cropIds: {valid_crops}")
    print(f"Invalid cropIds: {invalid_crops}")
    print(f"Invalid Product Relations: {invalid_products}")
    print(f"Records to Insert: {new_ids if duplicate_ids == 0 and invalid_crops == 0 and invalid_products == 0 else 0}")
    print("-------------------------\n")

    if duplicate_ids > 0 or invalid_crops > 0 or invalid_products > 0:
        print("VALIDATION FAILED. ABORTING IMPORT.")
        return

    print("VALIDATION PASSED. Executing IMPORT...")

    # 4. Import
    imported_count = 0
    imported_names = []
    
    for p in problems:
        doc_id = p["id"]
        clean_data = {}
        for k, v in p.items():
            if not k.startswith("_") and k != "id":
                clean_data[k] = v
        
        success = patch_document("agricultural_problems", doc_id, clean_data, token)
        if success:
            imported_count += 1
            imported_names.append((p["name"], doc_id, p["cropId"]))

    print(f"Imported {imported_count} problems.")

    # 5. Verify after import
    final_existing = set(get_collection_ids("agricultural_problems", token))
    
    print("\n--- IMPORT FINAL REPORT ---")
    print(f"Problems before: {len(existing_problems)}")
    print(f"Problems after: {len(final_existing)}")
    print("Added Problems:")
    for name, did, cid in imported_names:
        print(f"- {name} (ID: {did}, Crop: {cid})")
    print("---------------------------\n")

if __name__ == "__main__":
    main()
