from pymongo import MongoClient
import os
import pandas as pd
from dotenv import load_dotenv
import re


load_dotenv()

def get_mongo_collection(collection_name):
    mongo_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME")
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        print(f"Connected to MongoDB collection: {collection_name}.")
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def clean_val(val):
    if val == '-' or pd.isna(val) or val == '...':
        return None
    return float(val)

def find_province(province_name):
    # Pastikan input adalah string tunggal (bukan Series)
    # Jika province_name berasal dari baris Pandas, gunakan .strip()
    clean_name = re.sub(r'^PROV\.?\s+', '', str(province_name), flags=re.IGNORECASE).strip()
    clean_name = re.sub(r'^KEP\.?\s+', 'KEPULAUAN ', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'DI\.?\s+', 'DAERAH ISTIMEWA ', clean_name, flags=re.IGNORECASE)

    collection = get_mongo_collection("provinces")
    if collection is not None:
        # Menggunakan regex MongoDB untuk case-insensitive search
        result = collection.find_one({
            "properties.PROVINSI": { 
                "$regex": f"^{re.escape(clean_name)}$", 
                "$options": "i" 
            }
        })
        
        if result:
            # Kembalikan 'id' atau 'kode_prov' sesuai kebutuhan Anda
            return result.get('properties', {}).get('id') 
    return None

    