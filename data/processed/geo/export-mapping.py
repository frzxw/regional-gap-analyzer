from pymongo import MongoClient
from dotenv import load_dotenv
import json, os

export_path = "provinsi-mapping.json"

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")
collection_name = "provinces"

try:
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Query to fetch province properties
provinsi_properties = collection.find({}, {"properties": 1, "_id": 0})

records = []

for data in provinsi_properties:
    # Extract relevant fields
    id = data['properties']['id']
    provinsi = data['properties']['PROVINSI']
    mapping = {
        "kode_prov": id,
        "provinsi": provinsi
    }
    records.append(mapping)

    
try: 
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    print(f"Exporting data for province: {provinsi} with kode {id}")
except Exception as e:
    print(f"Error writing to file for province {provinsi}: {e}")