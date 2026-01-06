import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

def extract_json(df, tahun):
    prov_name = str(df['Unnamed: 0']).strip()

    province_id = utils.find_province(prov_name)
    if province_id is None:
        print(f"Province not found for: {prov_name}")
        return False

    json = {
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "indeks_pembangunan_manusia",
        "data": utils.clean_val(df[str(tahun)]),
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_tahun(tahun):
    for year in tahun:
        try:
            print(f"Processing year: {year}")
            bak_df = pd.read_csv(f'../../../raw/indeks-pembangunan-manusia/{year}.csv', skiprows=2)
            count = 0

            for index, row in bak_df.iterrows():
                if extract_json(row, year):
                    count += 1
                    
            print(f"Total records inserted for year {year}: {count}")
        except Exception as e:
            print(f"Error reading CSV file for year {year}: {e}")
        print(f"Finished processing year: {year}\n")

tahun = [
    '2020',
    '2021',
    '2022',
    '2023',
    '2024',
    '2025'
]

collection = utils.get_mongo_collection("indeks_pembangunan_manusia")
extract_tahun(tahun)