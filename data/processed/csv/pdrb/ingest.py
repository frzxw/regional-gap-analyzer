import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

def extract_json_adhk(df, tahun):
    prov_name = str(df['Provinsi']).strip()

    province_id = utils.find_province(prov_name)
    if province_id is None:
        print(f"Province not found for: {prov_name}")
        return False

    json = {
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "pdrb_per_kapita_adhk_2010",
        "data_ribu_rp": utils.clean_val(df["Produk Domestik Regional Bruto per Kapita HK (Ribu Rp)"]),
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_json_adhb(df, tahun):
    prov_name = str(df['Provinsi']).strip()

    province_id = utils.find_province(prov_name)
    if province_id is None:
        print(f"Province not found for: {prov_name}")
        return False

    json = {
        "province_id": province_id,
        "tahun": int(tahun),
        "indikator": "pdrb_per_kapita_adhb",
        "data_ribu_rp": utils.clean_val(df["Produk Domestik Regional Bruto per Kapita Atas Dasar Harga Berlaku (Ribu Rp)"]),
    }
    collection.insert_one(json)
    print(f"Inserted data for province: {prov_name}")
    return True

def extract_tahun(tahun):
    for year in tahun:
        try:
            print(f"Processing year: {year}")
            pdrb_adhb = pd.read_csv(f'../../../raw/pdrb/adhb/{year}.csv')
            pdrb_adhk = pd.read_csv(f'../../../raw/pdrb/adhk/{year}.csv')
            
            count = 0
            print(f"Extracting PDRB per Kapita ADHB for year {year}\n")
            for index, row in pdrb_adhb.iterrows():
                if extract_json_adhb(row, year):
                    count += 1
                    
            print(f"Total records inserted for year {year} ADHB: {count}")
            
            count = 0
            print(f"Extracting PDRB per Kapita ADHK for year {year}\n")
            for index, row in pdrb_adhk.iterrows():
                if extract_json_adhk(row, year):
                    count += 1
                    
            print(f"Total records inserted for year {year} ADHK: {count}")
        except Exception as e:
            print(f"Error reading CSV file for year {year}: {e}")
        print(f"Finished processing year: {year}\n")

tahun = [
    '2020',
    '2021',
    '2022',
    '2023',
    '2024'
]

collection = utils.get_mongo_collection("pdrb_per_kapita")
extract_tahun(tahun)