from dotenv import load_dotenv
import os
import json
import geopandas as gpd
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")

try:
    indonesia = gpd.read_file("../../geo/indonesia-38.json")
    geojson_data = indonesia.to_json()
    records = json.loads(geojson_data)["features"]
    print("GeoJSON data loaded.")
except Exception as e:
    print(f"Error loading GeoJSON data: {e}")

try:
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db["provinces"]
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")



if records:
    # 1. Import data provinsi asli (dengan geometry)
    collection.insert_many(records)
    print("GeoJSON data imported successfully.")

    # 2. Buat Dokumen Nasional (Tanpa Geometry)
    indonesia_national = {
        "id": "40", # Biasanya ID 0 digunakan untuk nasional
        "type": "Feature",
        "properties": {
            "id": "40",
            "PROVINSI": "INDONESIA",
            "is_national": True
        },
        "geometry": None # Atur ke None agar tidak ada data spasial
    }
    
    # Gunakan update_one dengan upsert agar tidak duplikat saat dijalankan ulang
    collection.update_one(
        {"properties.PROVINSI": "INDONESIA"},
        {"$set": indonesia_national},
        upsert=True
    )
    print("National 'Indonesia' record added without geometry.")

    collection.create_index([("geometry", "2dsphere")])
    print("2dsphere index created on geometry field.")