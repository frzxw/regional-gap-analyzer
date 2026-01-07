"""
Year-based scoring service - Business logic for year-based regional scoring.
Scores each collection individually and aggregates them.
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
import numpy as np

from app.db import get_database


class YearBasedScoringService:
    """
    Service for calculating year-based regional scores.
    
    Scores each collection individually using min-max normalization,
    then aggregates scores across all collections.
    """
    
    # Collection configurations
    # Format: collection_name: (field_to_score, lower_is_better)
    COLLECTION_CONFIGS = {
        "gini_ratio": {
            "field": "data_semester_2.total",  # Use semester 2 data (tahunan is null)
            "lower_is_better": True,
            "display_name": "Gini Ratio"
        },
        "indeks_pembangunan_manusia": {
            "field": "data",  # Direct float field
            "lower_is_better": False,
            "display_name": "Indeks Pembangunan Manusia"
        },
        "tingkat_pengangguran_terbuka": {
            "field": "data.agustus",  # Use August data (tahunan is null)
            "lower_is_better": True,
            "display_name": "Tingkat Pengangguran Terbuka"
        },
        "persentase_penduduk_miskin": {
            "field": "data_semester_2.total",  # Use semester 2 data
            "lower_is_better": True,
            "display_name": "Persentase Penduduk Miskin"
        },
        "pdrb_per_kapita": {
            "field": "data_ribu_rp",  # PDRB in thousands of rupiah
            "lower_is_better": False,
            "display_name": "PDRB Per Kapita"
        },
        "rata_rata_upah": {
            "field": "sektor.total.agustus",  # Total sector, August data (tahunan is null)
            "lower_is_better": False,
            "display_name": "Rata-rata Upah Bersih"
        },
        "inflasi_tahunan": {
            "field": "data_bulanan.desember",  # Use December data (tahunan is null)
            "lower_is_better": True,
            "display_name": "Inflasi Tahunan"
        },
        "indeks_harga_konsumen": {
            "field": "data_bulanan.desember",  # Use December data (tahunan is null)
            "lower_is_better": True,
            "display_name": "Indeks Harga Konsumen"
        },
        "angkatan_kerja": {
            "field": "data_agustus.persentase_bekerja_ak",  # Use August data for labor force participation
            "lower_is_better": False,
            "display_name": "Angkatan Kerja (% Bekerja)"
        }
    }
    
    @staticmethod
    def _get_field_value(doc: Dict, field_path: str) -> Optional[float]:
        """
        Get nested field value from document.
        
        Args:
            doc: MongoDB document
            field_path: Dot-notation field path (e.g., "data_tahunan.total")
            
        Returns:
            Field value or None if not found
        """
        keys = field_path.split(".")
        value = doc
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return float(value) if value is not None else None
    
    async def get_collection_data_for_year(
        self, 
        collection_name: str, 
        year: int
    ) -> List[Dict[str, Any]]:
        """
        Get all data from a collection for a specific year using MongoDB query.
        
        Args:
            collection_name: Name of the collection
            year: Year to filter
            
        Returns:
            List of documents with province_id and value
        """
        db = await get_database()
        collection = db[collection_name]
        
        config = self.COLLECTION_CONFIGS.get(collection_name)
        if not config:
            return []
        
        # Query MongoDB for the year
        cursor = collection.find({"tahun": year})
        
        results = []
        async for doc in cursor:
            value = self._get_field_value(doc, config["field"])
            if value is not None:
                results.append({
                    "province_id": doc.get("province_id"),
                    "value": value
                })
        
        return results
    
    @staticmethod
    def calculate_min_max_score(
        value: float,
        min_val: float,
        max_val: float,
        lower_is_better: bool
    ) -> float:
        """
        Calculate min-max normalized score (0-100).
        
        Args:
            value: Value to normalize
            min_val: Minimum value in dataset
            max_val: Maximum value in dataset
            lower_is_better: If True, lower values get higher scores
            
        Returns:
            Normalized score (0-100)
        """
        if max_val == min_val:
            return 50.0  # All values are the same
        
        # Normalize to 0-1
        normalized = (value - min_val) / (max_val - min_val)
        
        # Invert if lower is better
        if lower_is_better:
            normalized = 1 - normalized
        
        # Scale to 0-100
        return normalized * 100
    
    async def calculate_collection_scores(
        self,
        collection_name: str,
        year: int
    ) -> Dict[str, float]:
        """
        Calculate scores for all provinces in a collection for a specific year.
        
        Args:
            collection_name: Name of the collection
            year: Year to calculate scores for
            
        Returns:
            Dictionary mapping province_id to score
        """
        config = self.COLLECTION_CONFIGS.get(collection_name)
        if not config:
            return {}
        
        # Get data from MongoDB
        data = await self.get_collection_data_for_year(collection_name, year)
        
        if not data:
            return {}
        
        # Extract values for min-max calculation
        values = [item["value"] for item in data]
        min_val = min(values)
        max_val = max(values)
        
        # Calculate scores
        scores = {}
        for item in data:
            score = self.calculate_min_max_score(
                item["value"],
                min_val,
                max_val,
                config["lower_is_better"]
            )
            scores[item["province_id"]] = score
        
        return scores
    
    async def calculate_composite_score(
        self,
        province_id: str,
        year: int
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate composite score for a province by averaging all collection scores.
        
        Args:
            province_id: Province ID
            year: Year to calculate for
            
        Returns:
            Dictionary with composite score and breakdown
        """
        collection_scores = {}
        
        # Calculate score for each collection
        for collection_name in self.COLLECTION_CONFIGS.keys():
            scores = await self.calculate_collection_scores(collection_name, year)
            if province_id in scores:
                collection_scores[collection_name] = scores[province_id]
        
        if not collection_scores:
            return None
        
        # Calculate composite score (average)
        composite_score = sum(collection_scores.values()) / len(collection_scores)
        
        # Get province name from provinces collection (GeoJSON format)
        db = await get_database()
        province_name = "Unknown"
        
        # Query provinces collection with GeoJSON structure
        province_doc = await db.provinces.find_one({"properties.id": province_id})
        if province_doc and "properties" in province_doc and "PROVINSI" in province_doc["properties"]:
            province_name = province_doc["properties"]["PROVINSI"]
        
        return {
            "province_id": province_id,
            "province_name": province_name,
            "year": year,
            "composite_score": round(composite_score, 2),
            "collection_scores": {
                self.COLLECTION_CONFIGS[k]["display_name"]: round(v, 2)
                for k, v in collection_scores.items()
            },
            "collections_scored": len(collection_scores),
            "calculated_at": datetime.utcnow()
        }
    
    async def calculate_all_scores_for_year(
        self,
        year: int
    ) -> List[Dict[str, Any]]:
        """
        Calculate composite scores for all provinces in a specific year.
        
        Args:
            year: Year to calculate scores for
            
        Returns:
            List of score dictionaries sorted by composite_score (descending)
        """
        # Get all unique province IDs from any collection
        db = await get_database()
        province_ids = set()
        
        for collection_name in self.COLLECTION_CONFIGS.keys():
            collection = db[collection_name]
            cursor = collection.find({"tahun": year}, {"province_id": 1})
            async for doc in cursor:
                if "province_id" in doc:
                    pid = doc["province_id"]
                    # Filter: only include valid province IDs (2 digits, 11-97)
                    # Updated to include new Papua provinces: 95, 96, 97
                    if isinstance(pid, str) and len(pid) == 2 and pid.isdigit():
                        pid_int = int(pid)
                        if 11 <= pid_int <= 97:
                            province_ids.add(pid)
        
        # Calculate composite score for each province
        results = []
        for province_id in province_ids:
            score_data = await self.calculate_composite_score(province_id, year)
            if score_data:
                results.append(score_data)
        
        # Sort by composite score (descending) and add rank
        results.sort(key=lambda x: x["composite_score"], reverse=True)
        for idx, result in enumerate(results, 1):
            result["rank"] = idx
        
        return results
    
    async def get_score_breakdown(
        self,
        province_id: str,
        year: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get detailed score breakdown for a province.
        
        Args:
            province_id: Province ID
            year: Year
            
        Returns:
            Detailed breakdown with raw values and scores
        """
        db = await get_database()
        breakdown = {
            "province_id": province_id,
            "year": year,
            "collections": []
        }
        
        for collection_name, config in self.COLLECTION_CONFIGS.items():
            collection = db[collection_name]
            doc = await collection.find_one({
                "province_id": province_id,
                "tahun": year
            })
            
            if doc:
                raw_value = self._get_field_value(doc, config["field"])
                if raw_value is not None:
                    # Get all values for this year to calculate score
                    all_data = await self.get_collection_data_for_year(collection_name, year)
                    values = [item["value"] for item in all_data]
                    
                    if values:
                        min_val = min(values)
                        max_val = max(values)
                        score = self.calculate_min_max_score(
                            raw_value,
                            min_val,
                            max_val,
                            config["lower_is_better"]
                        )
                        
                        breakdown["collections"].append({
                            "collection": collection_name,
                            "display_name": config["display_name"],
                            "raw_value": raw_value,
                            "score": round(score, 2),
                            "min_value": min_val,
                            "max_value": max_val,
                            "lower_is_better": config["lower_is_better"]
                        })
        
        if not breakdown["collections"]:
            return None
        
        # Add composite score
        composite = await self.calculate_composite_score(province_id, year)
        if composite:
            breakdown["composite_score"] = composite["composite_score"]
            breakdown["province_name"] = composite["province_name"]
            breakdown["rank"] = composite.get("rank")
        
        return breakdown
    
    async def get_available_years(self) -> List[int]:
        """
        Get list of years that have data in any collection.
        
        Returns:
            Sorted list of years
        """
        db = await get_database()
        years = set()
        
        for collection_name in self.COLLECTION_CONFIGS.keys():
            collection = db[collection_name]
            cursor = collection.find({}, {"tahun": 1})
            async for doc in cursor:
                if "tahun" in doc:
                    years.add(doc["tahun"])
        
        return sorted(list(years))


# Singleton instance
year_based_scoring_service = YearBasedScoringService()
