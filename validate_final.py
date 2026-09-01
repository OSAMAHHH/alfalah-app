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
        with open("scripts/knowledge_base_final.json", "r", encoding="utf-8") as f:
            kb_final = json.load(f)
    except Exception as e:
        print(f"Failed to load file: {e}")
        return

    new_crops = kb_final.get("crops", [])
    new_problems = kb_final.get("agricultural_problems", [])
    
    print(f"Found {len(new_crops)} crops and {len(new_problems)} problems in JSON.")

    existing_crops = set(get_collection_ids("crops"))
    existing_problems = set(get_collection_ids("agricultural_problems"))
    
    print(f"Existing crops in DB: {len(existing_crops)}")
    print(f"Existing problems in DB: {len(existing_problems)}")

    duplicate_crop_ids = 0
    duplicate_prob_ids = 0
    invalid_crop_refs = 0
    invalid_types = 0

    allowed_types = ["disease", "pest", "nutrient_deficiency", "irrigation_problem", "soil_problem", "other"]
    
    all_valid_crop_ids = existing_crops.copy()

    for c in new_crops:
        if c["id"] in existing_crops:
            duplicate_crop_ids += 1
            print(f"DUPLICATE CROP ID: {c['id']}")
        else:
            all_valid_crop_ids.add(c["id"])

    for p in new_problems:
        if p["id"] in existing_problems:
            duplicate_prob_ids += 1
            print(f"DUPLICATE PROBLEM ID: {p['id']}")

        if p.get("cropId") not in all_valid_crop_ids:
            invalid_crop_refs += 1
            print(f"INVALID CROP ID REF: {p.get('cropId')} for {p['id']}")
            
        if p.get("type") not in allowed_types:
            invalid_types += 1
            print(f"INVALID TYPE: {p.get('type')} for {p['id']}")

    print("\n--- FINAL VALIDATION REPORT ---")
    print(f"New Crops in File: {len(new_crops)}")
    print(f"Existing Crops in DB: {len(existing_crops)}")
    print(f"Total Crops After Import: {len(existing_crops) + len(new_crops)}")
    print(f"Duplicate Crop IDs: {duplicate_crop_ids}")
    print(f"New Problems in File: {len(new_problems)}")
    print(f"Existing Problems in DB: {len(existing_problems)}")
    print(f"Total Problems After Import: {len(existing_problems) + len(new_problems)}")
    print(f"Duplicate Problem IDs: {duplicate_prob_ids}")
    print(f"Invalid Crop References: {invalid_crop_refs}")
    print(f"Invalid Problem Types: {invalid_types}")
    print("-------------------------------")
    
    if duplicate_crop_ids == 0 and duplicate_prob_ids == 0 and invalid_crop_refs == 0 and invalid_types == 0:
        print("VALIDATION_PASS")
    else:
        print("VALIDATION_FAIL")

if __name__ == "__main__":
    main()
