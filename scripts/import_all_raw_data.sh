#!/bin/bash

# Base API URL
API_URL="http://localhost:8000/api/imports/file"

# Resolve script directory to be robust regardless of execution path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DATA_DIR="$SCRIPT_DIR/../data/raw"

# Function to map folder to indicator code
get_indicator_code() {
    folder_name=$1
    case "$folder_name" in
        "gini-ratio") echo "gini_ratio" ;;
        "indeks-pembangunan-manusia") echo "ipm" ;;
        "tingkat-pengangguran-terbuka") echo "tpt" ;;
        "angkatan-kerja") echo "angkatan_kerja" ;;
        "persentase-penduduk-miskin") echo "persentase_penduduk_miskin" ;;
        "indeks-harga-konsumen") echo "ihk" ;;
        "inflasi-tahunan") echo "inflasi_tahunan" ;;
        "penduduk") echo "kependudukan" ;;
        "rata-rata-upah") echo "rata_rata_upah_bersih" ;;
        "pdrb") echo "pdrb_per_kapita" ;; 
        *) echo "unknown" ;;
    esac
}

echo "Starting Batch Import..."
echo "------------------------"

# Find all CSV files
find "$DATA_DIR" -type f -name "*.csv" | sort | while read -r file; do
    filename=$(basename "$file")
    parent_dir=$(basename "$(dirname "$file")")
    grandparent_dir=$(basename "$(dirname "$(dirname "$file")")")
    
    # Handle PDRB subfolders
    if [ "$grandparent_dir" == "pdrb" ]; then
        indicator="pdrb_per_kapita"
        if [ "$parent_dir" != "adhb" ]; then
            continue
        fi
    else
        indicator=$(get_indicator_code "$parent_dir")
    fi
    
    if [ "$indicator" == "unknown" ]; then
        continue
    fi
    
    # Extract year (assuming 20XX in filename)
    year=$(echo "$filename" | grep -oE '20[0-9]{2}')
    if [ -z "$year" ]; then
        echo "⚠️  Skipping $filename (No year found)"
        continue
    fi
    
    # Get absolute path
    abs_path=$(readlink -f "$file")
    
    echo -n "Importing $indicator / $year ... "
    
    # Use absolute path for file upload
    response=$(curl -X POST "$API_URL" \
      -H "accept: application/json" \
      -H "Content-Type: multipart/form-data" \
      -F "file=@$abs_path" \
      -F "indicator_code=$indicator" \
      -F "year=$year" \
      --fail --silent --show-error) # --fail causes curl to fail on server errors

    if [ $? -eq 0 ] && echo "$response" | grep -q '"success":true'; then
        count=$(echo "$response" | grep -o '"records_imported":[0-9]*' | cut -d':' -f2)
        echo "✅ OK ($count records)"
    else
        echo "❌ FAILED"
        echo "   Error: $response"
    fi
done

echo "------------------------"
echo "Batch Import Completed."
