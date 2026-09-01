import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PROJECT_ID = "alfalah-90856"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

def get_collection_ids(collection_name):
    url = f"{BASE_URL}/{collection_name}?pageSize=1000"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            docs = data.get("documents", [])
            return [doc["name"].split("/")[-1] for doc in docs]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        print(f"Error fetching {collection_name}: {e}")
        return []

def main():
    try:
        with open("scripts/batch_3_verified.json", "r") as f:
            batch3 = json.load(f)
    except Exception as e:
        print(f"Failed to load file: {e}")
        return

    problems = batch3.get("agricultural_problems", [])
    print(f"Found {len(problems)} problems in batch_3.")

    existing_problems = set(get_collection_ids("agricultural_problems"))
    existing_crops = set(get_collection_ids("crops"))
    
    print(f"Existing problems in DB: {len(existing_problems)}")
    print(f"Existing crops in DB: {len(existing_crops)}")

    duplicate_ids = 0
    new_ids = 0
    valid_crops = 0
    invalid_crops = 0
    valid_types = 0
    invalid_types = 0

    allowed_types = ["disease", "pest", "nutrient_deficiency", "irrigation_problem", "soil_problem", "other"]

    for p in problems:
        if p["id"] in existing_problems:
            duplicate_ids += 1
            print(f"DUPLICATE PROBLEM ID: {p['id']}")
        else:
            new_ids += 1

        if p.get("cropId") in existing_crops:
            valid_crops += 1
        else:
            invalid_crops += 1
            print(f"INVALID CROP ID: {p.get('cropId')} for {p['id']}")
            
        if p.get("type") in allowed_types:
            valid_types += 1
        else:
            invalid_types += 1
            print(f"INVALID TYPE: {p.get('type')} for {p['id']}")

    print("\n--- VALIDATION REPORT ---")
    print(f"Total Problems in File: {len(problems)}")
    print(f"New IDs: {new_ids}")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Valid cropIds: {valid_crops}")
    print(f"Invalid cropIds: {invalid_crops}")
    print(f"Valid types: {valid_types}")
    print(f"Invalid types: {invalid_types}")
    
    if duplicate_ids == 0 and invalid_crops == 0 and invalid_types == 0:
        print("VALIDATION_PASS")
    else:
        print("VALIDATION_FAIL")

if __name__ == "__main__":
    main()
