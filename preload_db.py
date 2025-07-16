import os
import requests
import hashlib
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import sqlite3

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
rebrickable_api_key = os.getenv("REBRICKABLE_API_KEY")
brickset_api_key = os.getenv("BRICKSET_API_KEY")
brickset_username = os.getenv("BRICKSET_USERNAME")
brickset_password = os.getenv("BRICKSET_PASSWORD")
brickowl_api_key = os.getenv("BRICKOWL_API_KEY")

# Initialize SQLite database
conn = sqlite3.connect("lego_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS lego_data (
        id TEXT PRIMARY KEY,
        source TEXT,
        name TEXT,
        details TEXT
    )
""")

# Function to generate unique ID for each record
def generate_unique_id(source, item_id):
    return hashlib.md5(f"{source}_{item_id}".encode()).hexdigest()

# 1. Fetch data from Rebrickable API
print("Fetching data from Rebrickable API...")
def fetch_rebrickable_sets():
    url = "https://rebrickable.com/api/v3/lego/sets/"
    headers = {"Authorization": f"key {rebrickable_api_key}"}
    all_sets = []
    page = 1
    while True:
        params = {"page": page, "page_size": 100, "ordering": "-set_num"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Rebrickable API error: {response.status_code} - {response.text}")
            break
        data = response.json()
        all_sets.extend(data["results"])
        print(f"Fetched page {page}, {len(data['results'])} sets")
        if not data.get("next"):
            break
        page += 1
    return all_sets

rebrickable_sets = fetch_rebrickable_sets()
for set_data in rebrickable_sets:
    set_id = set_data.get("set_num")
    name = set_data.get("name")
    details = json.dumps(set_data)
    unique_id = generate_unique_id("rebrickable", set_id)
    cursor.execute(
        "INSERT OR REPLACE INTO lego_data (id, source, name, details) VALUES (?, ?, ?, ?)",
        (unique_id, "rebrickable", name, details)
    )
print(f"Inserted {len(rebrickable_sets)} Rebrickable sets")

# 2. Fetch data from Brickset API
print("Fetching data from Brickset API...")
def get_brickset_user_hash():
    url = "https://brickset.com/api/v3.asmx/login"
    params = {
        "apiKey": brickset_api_key,
        "username": brickset_username,
        "password": brickset_password
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json().get("status") == "success":
        return response.json().get("hash")
    print(f"Brickset login error: {response.status_code} - {response.text}")
    return None

def fetch_brickset_sets():
    user_hash = get_brickset_user_hash()
    if not user_hash:
        print("Failed to authenticate with Brickset API")
        return []
    url = "https://brickset.com/api/v3.asmx/getSets"
    params = {
        "apiKey": brickset_api_key,
        "userHash": user_hash,
        "params": json.dumps({"year": 2024})
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json().get("status") == "success":
        return response.json().get("sets", [])
    print(f"Brickset API error: {response.status_code} - {response.text}")
    return []

brickset_sets = fetch_brickset_sets()
for set_data in brickset_sets:
    set_id = set_data.get("number")
    name = set_data.get("name")
    details = json.dumps(set_data)
    unique_id = generate_unique_id("brickset", set_id)
    cursor.execute(
        "INSERT OR REPLACE INTO lego_data (id, source, name, details) VALUES (?, ?, ?, ?)",
        (unique_id, "brickset", name, details)
    )
print(f"Inserted {len(brickset_sets)} Brickset sets")

# 3. Fetch data from BrickOwl API
print("Fetching data from BrickOwl API...")
def fetch_brickowl_sets():
    url = "https://api.brickowl.com/v1/catalog/list"
    params = {"key": brickowl_api_key, "type": "Set"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    print(f"BrickOwl API error: {response.status_code} - {response.text}")
    return []

brickowl_sets = fetch_brickowl_sets()
for set_data in brickowl_sets:
    set_id = set_data.get("boid")
    name = set_data.get("name")
    details = json.dumps(set_data)
    unique_id = generate_unique_id("brickowl", set_id)
    cursor.execute(
        "INSERT OR REPLACE INTO lego_data (id, source, name, details) VALUES (?, ?, ?, ?)",
        (unique_id, "brickowl", name, details)
    )
print(f"Inserted {len(brickowl_sets)} BrickOwl sets")

# Commit SQLite changes
conn.commit()
print("SQLite database committed")

# Load data into ChromaDB
print("Building ChromaDB index...")
texts = [row[3] for row in cursor.execute("SELECT details FROM lego_data").fetchall()]
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma.from_texts(texts, embeddings, persist_directory="./chroma_db")
vectorstore.persist()
print("ChromaDB index built and persisted")

# Cleanup
conn.close()
print("Database connection closed. Preloading complete.")