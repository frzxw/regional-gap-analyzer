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
        "indikator": "gini_ratio",
        "data_semester_1": {
            "perkotaan": utils.clean_val(df['Semester 1 (Maret)']),
            "perdesaan": utils.clean_val(df['Semester 1 (Maret).1']),
            "total": utils.clean_val(df['Semester 1 (Maret).2'])
        },
        "data_semester_2": {
            "perkotaan": utils.clean_val(df['Semester 2 (September)']),
            "perdesaan": utils.clean_val(df['Semester 2 (September).1']),
            "total": utils.clean_val(df['Semester 2 (September).2'])
        },
        "data_tahunan": {
            "perkotaan": utils.clean_val(df['Tahunan']),
            "perdesaan": utils.clean_val(df['Tahunan.1']),
            "total": utils.clean_val(df['Tahunan.2'])
        }
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_tahun(tahun):
    for year in tahun:
        try:
            print(f"Processing year: {year}")
            bak_df = pd.read_csv(f'../../../raw/gini-ratio/{year}.csv', skiprows=4)
            count = 0

            for index, row in bak_df.iterrows():
                if extract_json(row, year):
                    count += 1
                    
            print(f"Total records inserted for year {year}: {count}")
        except Exception as e:
            print(f"Error reading CSV file for year {year}: {e}")
        print(f"Finished processing year: {year}")
tahun = [
    '2020',
    '2021',
    '2022',
    '2023',
    '2024',
    '2025'
]

collection = utils.get_mongo_collection("gini_ratio")
extract_tahun(tahun)