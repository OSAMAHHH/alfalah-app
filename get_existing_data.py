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
    crops = get_collection_ids("crops")
    problems = get_collection_ids("agricultural_problems")
    products = get_collection_ids("products")
    
    with open("existing_data.json", "w") as f:
        json.dump({"crops": crops, "problems": problems, "products": products}, f)
    
    print(f"Existing Crops: {len(crops)}")
    print(f"Existing Problems: {len(problems)}")
    print(f"Existing Products: {len(products)}")

if __name__ == "__main__":
    main()
