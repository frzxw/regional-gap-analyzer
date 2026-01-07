# Regional Gap Analyzer - Complete API Reference

**Version:** 0.1.0  
**Base URL:** `http://localhost:8000`  
**API Prefix:** `/api/v1` (for data endpoints)

---

## Table of Contents

1. [Health & Status](#health--status)
2. [Regions Management](#regions-management)
3. [Geographic Data](#geographic-data)
4. [Scores & Rankings](#scores--rankings)
5. [Configuration](#configuration)
6. [Data Indicators](#data-indicators)
7. [Data Sources](#data-sources)
8. [Alerts & Notifications](#alerts--notifications)
9. [Data Import](#data-import)
10. [Data Type Endpoints (CRUD)](#data-type-endpoints-crud)
11. [Unemployment Analysis](#unemployment-analysis)
12. [Error Handling](#error-handling)

---

## Health & Status

### 1. Basic Health Check
**GET** `/health`

Basic health check to verify API is running.

**Response (200):**
```json
{
  "status": "ok"
}
```

---

### 2. Detailed Health Check
**GET** `/health/detailed`

Health check including database connectivity.

**Response (200):**
```json
{
  "status": "ok",
  "database": "connected"
}
```

**Response (200 - Degraded):**
```json
{
  "status": "degraded",
  "database": "disconnected"
}
```

---

### 3. Full Health Check
**GET** `/health/full`

Complete health status with version and timestamp.

**Response (200):**
```json
{
  "status": "ok",
  "database": "connected",
  "version": "0.1.0",
  "timestamp": "2025-01-15T10:30:45.123456+00:00"
}
```

---

## Regions Management

### 1. List All Regions
**GET** `/api/v1/regions`

Returns paginated list of all Indonesian provinces with GeoJSON format.

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| page | integer | 1 | ≥1 | Page number (1-indexed) |
| page_size | integer | 20 | 1-100 | Items per page |

**Response (200):**
```json
{
  "regions": [
    {
      "id": "31",
      "type": "Feature",
      "properties": {
        "KODE_PROV": "31",
        "PROVINSI": "DKI Jakarta",
        "is_national": false
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
      },
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  ],
  "total": 38,
  "page": 1,
  "page_size": 20
}
```

---

### 2. Get Region by Code
**GET** `/api/v1/regions/{region_code}`

Get a single region by its KODE_PROV code.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV (e.g., "31" for Jakarta) |

**Response (200):**
```json
{
  "id": "31",
  "type": "Feature",
  "properties": {
    "KODE_PROV": "31",
    "PROVINSI": "DKI Jakarta"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
  },
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Error Responses:**
- **404:** Region not found

---

### 3. Create Region
**POST** `/api/v1/regions`

Create a new region record.

**Request Body:**
```json
{
  "id": "31",
  "type": "Feature",
  "properties": {
    "KODE_PROV": "31",
    "PROVINSI": "DKI Jakarta"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[106.7, -6.1], [106.9, -6.1], [106.9, -6.3], [106.7, -6.3], [106.7, -6.1]]]
  }
}
```

**Response (201):**
```json
{
  "message": "Region '31' (PROVINSI: 'DKI Jakarta') created successfully"
}
```

**Error Responses:**
- **409:** Region with same KODE_PROV already exists

---

### 4. Update Region
**PUT** `/api/v1/regions/{region_code}`

Update region data. **Only PROVINSI field can be modified** (for data integrity).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV to update |

**Request Body:**
```json
{
  "PROVINSI": "DKI Jakarta Raya"
}
```

**Response (200):**
```json
{
  "message": "Region '31' (PROVINSI: 'DKI Jakarta Raya') updated successfully"
}
```

**Error Responses:**
- **404:** Region not found

---

### 5. Delete Region
**DELETE** `/api/v1/regions/{region_code}`

Delete a region by its code.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV to delete |

**Response (200):**
```json
{
  "message": "Region '31' deleted successfully"
}
```

**Error Responses:**
- **404:** Region not found

---

## Geographic Data

All geographic endpoints support choropleth map visualization and boundary queries.

### 1. Get Provinces GeoJSON
**GET** `/geo/provinces`

Get base GeoJSON for all Indonesian provinces (for map initialization).

**Response (200):**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "31",
      "properties": {
        "KODE_PROV": "31",
        "PROVINSI": "DKI Jakarta"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    }
  ]
}
```

---

### 2. Get Choropleth Data
**GET** `/geo/choropleth`

Get GeoJSON with score data for choropleth map visualization.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | latest | Year for score data |
| metric | string | composite_score | Metric to display |

**Response (200):**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "KODE_PROV": "31",
        "PROVINSI": "DKI Jakarta",
        "composite_score": 75.5,
        "ranking": 1
      },
      "geometry": {...}
    }
  ]
}
```

---

### 3. Get Province Boundary
**GET** `/geo/province/{region_code}`

Get GeoJSON feature for a specific province.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV (e.g., "31") |

**Response (200):**
```json
{
  "type": "Feature",
  "properties": {
    "KODE_PROV": "31",
    "PROVINSI": "DKI Jakarta"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [...]
  }
}
```

**Error Responses:**
- **404:** Province not found

---

### 4. Get Color Scale
**GET** `/geo/color-scale`

Get color scale configuration for map legend.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| min_value | float | 0 | Minimum value |
| max_value | float | 100 | Maximum value |
| palette | string | RdYlGn | Color palette (RdYlGn, YlOrRd, Viridis, etc.) |

**Response (200):**
```json
{
  "palette": "RdYlGn",
  "min": 0,
  "max": 100,
  "stops": [
    {"value": 0, "color": "#a50026"},
    {"value": 25, "color": "#fee08b"},
    {"value": 50, "color": "#ffffbf"},
    {"value": 75, "color": "#a6d96a"},
    {"value": 100, "color": "#006837"}
  ]
}
```

---

## Scores & Rankings

### 1. List Composite Scores
**GET** `/scores`

List composite scores with optional year filter.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | null | Filter by year (all years if null) |
| skip | integer | 0 | Skip N records |
| limit | integer | 50 | Limit results (max 100) |

**Response (200):**
```json
[
  {
    "region_code": "31",
    "year": 2023,
    "composite_score": 75.5,
    "ranking": 1,
    "trend": "improving",
    "components": {
      "hdi": 80.2,
      "poverty_rate": 70.1,
      "gini": 65.3
    }
  }
]
```

---

### 2. Get Regional Rankings
**GET** `/scores/rankings`

Get region rankings by composite score for a specific year.

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| year | integer | latest | 1990-2030 | Year (latest if not specified) |
| limit | integer | 38 | 1-100 | Number of top regions |

**Response (200):**
```json
{
  "year": 2023,
  "rankings": [
    {
      "rank": 1,
      "region_code": "31",
      "provinsi": "DKI Jakarta",
      "score": 85.3
    },
    {
      "rank": 2,
      "region_code": "12",
      "provinsi": "Surabaya",
      "score": 82.1
    }
  ]
}
```

---

### 3. Get Top & Bottom Performers
**GET** `/scores/top-bottom`

Get top and bottom performing regions for inequality analysis.

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| year | integer | latest | 1990-2030 | Year |
| count | integer | 5 | 1-10 | Number of top/bottom regions |

**Response (200):**
```json
{
  "year": 2023,
  "top_performers": [
    {
      "rank": 1,
      "region_code": "31",
      "provinsi": "DKI Jakarta",
      "score": 85.3
    }
  ],
  "bottom_performers": [
    {
      "rank": 38,
      "region_code": "53",
      "provinsi": "Nusa Tenggara Timur",
      "score": 35.2
    }
  ]
}
```

---

### 4. Get Region Score
**GET** `/scores/region/{region_code}`

Get score details for a specific region.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV |

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | latest | Specific year |

**Response (200):**
```json
{
  "region_code": "31",
  "provinsi": "DKI Jakarta",
  "year": 2023,
  "composite_score": 85.3,
  "ranking": 1,
  "breakdown": {
    "hdi": {"value": 80.2, "weight": 0.25},
    "poverty_rate": {"value": 70.1, "weight": 0.20},
    "gini_ratio": {"value": 65.3, "weight": 0.15}
  }
}
```

**Error Responses:**
- **404:** No score found for region

---

### 5. Get Region Score History
**GET** `/scores/region/{region_code}/history`

Get score history for a region over time.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV |

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| start_year | integer | 2015 | ≥1990 | Start year |
| end_year | integer | 2024 | ≤2030 | End year |

**Response (200):**
```json
{
  "region_code": "31",
  "start_year": 2015,
  "end_year": 2024,
  "history": [
    {"year": 2015, "score": 70.2, "ranking": 5},
    {"year": 2016, "score": 71.5, "ranking": 4},
    {"year": 2023, "score": 85.3, "ranking": 1}
  ]
}
```

---

### 6. Get Gap Analysis
**GET** `/scores/gap-analysis`

Get gap analysis showing disparity between regions.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | latest | Year for analysis |

**Response (200):**
```json
{
  "year": 2023,
  "gap_index": 0.342,
  "national_average": 60.5,
  "highest_score": 85.3,
  "lowest_score": 35.2,
  "standard_deviation": 12.1,
  "coefficient_variation": 0.20,
  "disparity_summary": {
    "high_inequality_regions": 8,
    "medium_inequality_regions": 15,
    "low_inequality_regions": 15
  }
}
```

---

### 7. Recalculate Scores
**POST** `/scores/recalculate`

Trigger score recalculation for a year.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | latest | Year to recalculate |
| force | boolean | false | Force recalculation |

**Response (200):**
```json
{
  "success": true,
  "message": "Scores recalculated for year 2023",
  "records_processed": 38,
  "duration_seconds": 2.5
}
```

---

### 8. Get Available Years
**GET** `/scores/years`

Get list of years with available score data.

**Response (200):**
```json
{
  "years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
}
```

---

## Configuration

### 1. List All Configurations
**GET** `/configs`

List all configuration entries in the system.

**Response (200):**
```json
{
  "configs": [
    {
      "key": "indicator_weights",
      "value": {
        "HDI": 0.25,
        "POVERTY_RATE": 0.20,
        "GRDP_CAPITA": 0.20,
        "GINI": 0.15,
        "UNEMPLOYMENT": 0.10,
        "LITERACY": 0.10
      }
    }
  ]
}
```

---

### 2. Get Specific Configuration
**GET** `/configs/{key}`

Get a specific configuration value.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| key | string | Configuration key |

**Response (200):**
```json
{
  "key": "indicator_weights",
  "value": {
    "HDI": 0.25,
    "POVERTY_RATE": 0.20
  }
}
```

**Error Responses:**
- **404:** Config key not found

---

### 3. Update Configuration
**PUT** `/configs/{key}`

Set or update a configuration value.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| key | string | Configuration key |

**Request Body:**
```json
{
  "key": "indicator_weights",
  "value": {
    "HDI": 0.25,
    "POVERTY_RATE": 0.20
  }
}
```

**Response (200):**
```json
{
  "key": "indicator_weights",
  "value": {...},
  "updated_at": "2025-01-15T10:30:45.123456+00:00"
}
```

---

### 4. Delete Configuration
**DELETE** `/configs/{key}`

Delete a configuration entry.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| key | string | Configuration key |

**Response (204):** No content

**Error Responses:**
- **404:** Config key not found

---

### 5. Get Indicator Weights
**GET** `/configs/weights/indicators`

Get current indicator weights for scoring calculation.

**Response (200):**
```json
{
  "HDI": 0.25,
  "POVERTY_RATE": 0.20,
  "GRDP_CAPITA": 0.20,
  "GINI": 0.15,
  "UNEMPLOYMENT": 0.10,
  "LITERACY": 0.10
}
```

---

### 6. Update Indicator Weights
**PUT** `/configs/weights/indicators`

Update indicator weights. **Weights MUST sum to 1.0**.

**Request Body:**
```json
{
  "HDI": 0.30,
  "POVERTY_RATE": 0.25,
  "GRDP_CAPITA": 0.20,
  "GINI": 0.15,
  "UNEMPLOYMENT": 0.10
}
```

**Response (200):**
```json
{
  "key": "indicator_weights",
  "value": {...},
  "description": "Indicator weights for composite score calculation"
}
```

**Error Responses:**
- **400:** Weights do not sum to 1.0

---

### 7. Get Alert Thresholds
**GET** `/configs/thresholds/alerts`

Get alert threshold configuration.

**Response (200):**
```json
{
  "critical_score": 30,
  "warning_score": 50,
  "rank_drop_critical": 5,
  "rank_drop_warning": 3
}
```

---

### 8. Update Alert Thresholds
**PUT** `/configs/thresholds/alerts`

Update alert threshold configuration.

**Request Body:**
```json
{
  "critical_score": 25,
  "warning_score": 45,
  "rank_drop_critical": 10,
  "rank_drop_warning": 5
}
```

**Response (200):**
```json
{
  "key": "alert_thresholds",
  "value": {...},
  "description": "Thresholds for alert generation"
}
```

---

## Data Indicators

### 1. List Indicators
**GET** `/indicators`

List indicator records with optional filters.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| region_code | string | null | Filter by region |
| indicator_code | string | null | Filter by indicator type (HDI, GINI, etc.) |
| year | integer | null | Filter by year |
| skip | integer | 0 | Skip N records |
| limit | integer | 50 | Limit results (max 100) |

**Response (200):**
```json
{
  "items": [
    {
      "_id": "...",
      "region_code": "31",
      "indicator_code": "HDI",
      "year": 2023,
      "value": 80.2,
      "unit": "index",
      "created_at": "2025-01-15T10:30:45.123456+00:00"
    }
  ],
  "total": 456,
  "skip": 0,
  "limit": 50
}
```

---

### 2. List Indicator Definitions
**GET** `/indicators/definitions`

Get list of all indicator definitions with metadata.

**Response (200):**
```json
[
  {
    "code": "HDI",
    "name": "Human Development Index",
    "description": "Composite measure of life expectancy, education, and per capita income",
    "unit": "index (0-100)",
    "data_source": "UNDP / BPS",
    "last_updated": "2025-01-15"
  },
  {
    "code": "GINI",
    "name": "Gini Ratio",
    "description": "Income inequality coefficient",
    "unit": "ratio (0-100)",
    "data_source": "BPS",
    "last_updated": "2025-01-15"
  }
]
```

---

### 3. Get Region Indicators
**GET** `/indicators/region/{region_code}`

Get all indicators for a specific region.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region_code | string | KODE_PROV |

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | null | Specific year (all if null) |

**Response (200):**
```json
{
  "region_code": "31",
  "indicators": [
    {
      "code": "HDI",
      "name": "Human Development Index",
      "value": 80.2,
      "year": 2023
    },
    {
      "code": "GINI",
      "name": "Gini Ratio",
      "value": 0.385,
      "year": 2023
    }
  ]
}
```

**Error Responses:**
- **404:** No indicators found for region

---

### 4. Get Indicator History
**GET** `/indicators/{indicator_code}/history`

Get historical time series for an indicator.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| indicator_code | string | Indicator code (HDI, GINI, etc.) |

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| region_code | string | null | - | Filter by specific region |
| start_year | integer | 2010 | ≥1990 | Start year |
| end_year | integer | 2024 | ≤2030 | End year |

**Response (200):**
```json
{
  "indicator_code": "HDI",
  "region_code": "31",
  "start_year": 2010,
  "end_year": 2024,
  "data": [
    {"year": 2010, "value": 70.2},
    {"year": 2011, "value": 71.5},
    {"year": 2023, "value": 80.2}
  ]
}
```

---

### 5. Create Indicator
**POST** `/indicators`

Create a new indicator record.

**Request Body:**
```json
{
  "region_code": "31",
  "indicator_code": "HDI",
  "year": 2023,
  "value": 80.2,
  "unit": "index",
  "source_id": "source_123"
}
```

**Response (201):**
```json
{
  "_id": "...",
  "region_code": "31",
  "indicator_code": "HDI",
  "year": 2023,
  "value": 80.2,
  "unit": "index",
  "created_at": "2025-01-15T10:30:45.123456+00:00"
}
```

---

### 6. Update Indicator
**PUT** `/indicators/{indicator_id}`

Update an existing indicator record.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| indicator_id | string | Indicator MongoDB _id |

**Request Body:**
```json
{
  "value": 81.5
}
```

**Response (200):**
```json
{
  "_id": "...",
  "region_code": "31",
  "indicator_code": "HDI",
  "year": 2023,
  "value": 81.5,
  "updated_at": "2025-01-15T10:30:45.123456+00:00"
}
```

**Error Responses:**
- **404:** Indicator not found

---

### 7. Delete Indicator
**DELETE** `/indicators/{indicator_id}`

Delete an indicator record.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| indicator_id | string | Indicator MongoDB _id |

**Response (204):** No content

**Error Responses:**
- **404:** Indicator not found

---

## Data Sources

### 1. List Data Sources
**GET** `/sources`

List all data sources.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | integer | 0 | Skip N records |
| limit | integer | 50 | Limit results (max 100) |

**Response (200):**
```json
{
  "items": [
    {
      "_id": "...",
      "name": "BPS Annual Statistics 2023",
      "type": "file",
      "url": "https://bps.go.id/...",
      "description": "Official BPS national statistics",
      "created_at": "2025-01-15T10:30:45.123456+00:00",
      "imported_records": 456
    }
  ],
  "total": 12,
  "skip": 0,
  "limit": 50
}
```

---

### 2. Get Data Source
**GET** `/sources/{source_id}`

Get a specific data source by ID.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_id | string | Source MongoDB _id |

**Response (200):**
```json
{
  "_id": "...",
  "name": "BPS Annual Statistics 2023",
  "type": "file",
  "url": "https://bps.go.id/...",
  "description": "Official BPS national statistics",
  "created_at": "2025-01-15T10:30:45.123456+00:00"
}
```

**Error Responses:**
- **404:** Source not found

---

### 3. Create Data Source
**POST** `/sources`

Create a new data source record.

**Request Body:**
```json
{
  "name": "BPS Annual Statistics 2023",
  "type": "file",
  "url": "https://bps.go.id/...",
  "description": "Official BPS national statistics"
}
```

**Response (201):**
```json
{
  "_id": "...",
  "name": "BPS Annual Statistics 2023",
  "type": "file",
  "url": "https://bps.go.id/...",
  "created_at": "2025-01-15T10:30:45.123456+00:00"
}
```

---

### 4. Update Data Source
**PUT** `/sources/{source_id}`

Update a data source.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_id | string | Source MongoDB _id |

**Request Body:**
```json
{
  "name": "BPS Annual Statistics 2024",
  "description": "Updated to 2024 data"
}
```

**Response (200):**
```json
{
  "_id": "...",
  "name": "BPS Annual Statistics 2024",
  "updated_at": "2025-01-15T10:30:45.123456+00:00"
}
```

**Error Responses:**
- **404:** Source not found

---

### 5. Delete Data Source
**DELETE** `/sources/{source_id}`

Delete a data source.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_id | string | Source MongoDB _id |

**Response (204):** No content

**Error Responses:**
- **404:** Source not found

---

### 6. Get Source Indicators
**GET** `/sources/{source_id}/indicators`

Get all indicators from a specific source.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_id | string | Source MongoDB _id |

**Response (200):**
```json
{
  "source": {
    "_id": "...",
    "name": "BPS Annual Statistics 2023"
  },
  "indicators": [
    {
      "region_code": "31",
      "indicator_code": "HDI",
      "year": 2023,
      "value": 80.2
    }
  ],
  "count": 456
}
```

**Error Responses:**
- **404:** Source not found

---

## Alerts & Notifications

### 1. List Alerts
**GET** `/alerts`

List alerts with optional filters.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| region_code | string | null | Filter by region |
| severity | string | null | Filter by severity (low, medium, high, critical) |
| status | string | null | Filter by status (open, acknowledged, resolved) |
| skip | integer | 0 | Skip N records |
| limit | integer | 50 | Limit results (max 100) |

**Response (200):**
```json
{
  "items": [
    {
      "_id": "...",
      "region_code": "31",
      "severity": "high",
      "status": "open",
      "title": "Significant inequality increase",
      "description": "Regional gap index increased by 15%",
      "created_at": "2025-01-15T10:30:45.123456+00:00"
    }
  ],
  "total": 12,
  "skip": 0,
  "limit": 50
}
```

---

### 2. Get Active Alerts
**GET** `/alerts/active`

Get currently active (unacknowledged) alerts.

**Query Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| region_code | string | null | - | Filter by region |
| limit | integer | 20 | 1-50 | Max alerts |

**Response (200):**
```json
{
  "alerts": [
    {
      "_id": "...",
      "region_code": "31",
      "severity": "critical",
      "title": "Critical inequality detected",
      "created_at": "2025-01-15T10:30:45.123456+00:00"
    }
  ],
  "count": 3
}
```

---

### 3. Get Alerts Summary
**GET** `/alerts/summary`

Get summary of alerts by severity and region.

**Response (200):**
```json
{
  "by_severity": {
    "critical": 2,
    "high": 5,
    "medium": 8,
    "low": 3
  },
  "by_status": {
    "open": 10,
    "acknowledged": 5,
    "resolved": 3
  },
  "by_region": {
    "31": 3,
    "51": 2,
    "53": 5
  }
}
```

---

### 4. Get Alert Details
**GET** `/alerts/{alert_id}`

Get a specific alert by ID.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| alert_id | string | Alert MongoDB _id |

**Response (200):**
```json
{
  "_id": "...",
  "region_code": "31",
  "severity": "high",
  "status": "open",
  "title": "Significant inequality increase",
  "description": "Regional gap index increased by 15%",
  "created_at": "2025-01-15T10:30:45.123456+00:00",
  "acknowledged_at": null
}
```

**Error Responses:**
- **404:** Alert not found

---

### 5. Acknowledge Alert
**POST** `/alerts/{alert_id}/acknowledge`

Acknowledge an alert (mark as reviewed).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| alert_id | string | Alert MongoDB _id |

**Request Body:**
```json
{
  "acknowledged_by": "user@example.com",
  "notes": "Noted, investigating further"
}
```

**Response (200):**
```json
{
  "_id": "...",
  "status": "acknowledged",
  "acknowledged_at": "2025-01-15T10:30:45.123456+00:00",
  "acknowledged_by": "user@example.com"
}
```

**Error Responses:**
- **404:** Alert not found

---

### 6. Resolve Alert
**POST** `/alerts/{alert_id}/resolve`

Mark an alert as resolved.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| alert_id | string | Alert MongoDB _id |

**Request Body:**
```json
{
  "resolved_by": "user@example.com",
  "resolution_notes": "Issue addressed through policy intervention"
}
```

**Response (200):**
```json
{
  "_id": "...",
  "status": "resolved",
  "resolved_at": "2025-01-15T10:30:45.123456+00:00",
  "resolved_by": "user@example.com"
}
```

**Error Responses:**
- **404:** Alert not found

---

### 7. Generate Alerts
**POST** `/alerts/generate`

Generate alerts based on current data and thresholds.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| year | integer | latest | Year to generate alerts for |

**Response (200):**
```json
{
  "generated": 5,
  "updated": 2,
  "message": "Alert generation completed"
}
```

---

### 8. Delete Alert
**DELETE** `/alerts/{alert_id}`

Delete an alert.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| alert_id | string | Alert MongoDB _id |

**Response (204):** No content

**Error Responses:**
- **404:** Alert not found

---

## Data Import

### 1. Import from File
**POST** `/imports/file`

Import indicator data from an uploaded file (CSV, Excel, or JSON).

**Form Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | CSV, XLSX, XLS, or JSON file |
| indicator_code | string | Yes | Indicator code (HDI, GINI, etc.) |
| year | integer | Yes | Year of the data |
| source_name | string | No | Data source name |
| source_type | string | No | Source type (default: "file") |

**Response (200):**
```json
{
  "success": true,
  "message": "Import completed successfully",
  "records_processed": 38,
  "records_imported": 38,
  "duration_seconds": 2.5
}
```

**Error Responses:**
- **400:** Invalid file type or import error

---

### 2. Validate Import File
**POST** `/imports/validate`

Validate an import file without actually importing.

**Form Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | CSV, XLSX, XLS, or JSON file |

**Response (200):**
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Column 'unit' not found"],
  "preview": [
    {"region": "31", "value": "80.2"},
    {"region": "51", "value": "78.5"}
  ],
  "row_count": 38
}
```

**Error Responses:**
- **400:** Invalid file type

---

### 3. Import Batch
**POST** `/imports/batch`

Import a batch of indicator records programmatically.

**Request Body:**
```json
{
  "indicators": [
    {
      "region_code": "31",
      "indicator_code": "HDI",
      "year": 2023,
      "value": 80.5
    },
    {
      "region_code": "51",
      "indicator_code": "HDI",
      "year": 2023,
      "value": 78.2
    }
  ],
  "source_name": "BPS Import 2025",
  "source_id": "source_123",
  "upsert": true
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Batch import completed",
  "inserted": 38,
  "updated": 0,
  "failed": 0
}
```

**Error Responses:**
- **400:** Invalid batch format

---

### 4. Rollback Import
**POST** `/imports/rollback/{source_id}`

Rollback an import by deleting all indicators from a source.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| source_id | string | Source MongoDB _id |

**Response (200):**
```json
{
  "success": true,
  "message": "Import rolled back",
  "records_deleted": 38
}
```

**Error Responses:**
- **404:** Source not found

---

### 5. Get Import History
**GET** `/imports/history`

Get history of import operations.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | integer | 0 | Skip N records |
| limit | integer | 20 | Limit results (max 50) |

**Response (200):**
```json
{
  "imports": [
    {
      "_id": "...",
      "name": "BPS Annual Statistics 2023",
      "type": "file",
      "created_at": "2025-01-15T10:30:45.123456+00:00",
      "record_count": 38
    }
  ],
  "total": 15
}
```

---

## Data Type Endpoints (CRUD)

Each data type has a consistent CRUD interface. Available data types are:

- Angkatan Kerja (Labor Force)
- Gini Ratio (Income Inequality)
- Indeks Harga Konsumen (Consumer Price Index)
- Indeks Pembangunan Manusia (Human Development Index)
- Inflasi Tahunan (Annual Inflation)
- Kependudukan (Population)
- PDRB Per Kapita (GRDP Per Capita)
- Persentase Penduduk Miskin (Poverty Rate)
- Rata-rata Upah (Average Wage)
- Tingkat Pengangguran Terbuka (Open Unemployment Rate)

### Common CRUD Pattern

#### List Records
**GET** `/api/v1/{resource-name}`

List all records for a data type.

**Response (200):**
```json
{
  "data": [
    {
      "_id": "...",
      "province_id": "31",
      "tahun": 2023,
      "value": 80.5
    }
  ],
  "total": 456,
  "page": 1,
  "page_size": 20
}
```

---

#### Create Record
**POST** `/api/v1/{resource-name}`

Create a new record.

**Request Body:**
```json
{
  "province_id": "31",
  "tahun": 2023,
  "value": 80.5
}
```

**Response (201):**
```json
{
  "message": "Data created successfully"
}
```

**Error Responses:**
- **409:** Record already exists

---

#### Update Record
**PUT** `/api/v1/{resource-name}/{province_id}/{tahun}`

Update an existing record.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| province_id | string | Province ID |
| tahun | integer | Year |

**Request Body:**
```json
{
  "value": 81.5
}
```

**Response (200):**
```json
{
  "message": "Data updated successfully"
}
```

**Error Responses:**
- **404:** Record not found

---

#### Delete Record
**DELETE** `/api/v1/{resource-name}/{province_id}/{tahun}`

Delete a record.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| province_id | string | Province ID |
| tahun | integer | Year |

**Response (200):**
```json
{
  "message": "Data deleted successfully"
}
```

**Error Responses:**
- **404:** Record not found

---

#### Import CSV
**POST** `/api/v1/{resource-name}/import-csv`

Import data from CSV file.

**Form Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | CSV file |
| tahun | integer | Yes | Year of data |

**Response (200):**
```json
{
  "success": true,
  "message": "Import completed",
  "records_imported": 38,
  "records_failed": 0,
  "source_id": "..."
}
```

**Error Responses:**
- **400:** Invalid file format

---

#### PDRB-Specific Endpoints

PDRB Per Kapita has two import variants for different price bases:

**POST** `/api/v1/pdrb-per-kapita/import-csv-adhb`

Import ADHB (Harga Dasar Berlaku) data.

**POST** `/api/v1/pdrb-per-kapita/import-csv-adhk`

Import ADHK (Harga Dasar Konstan) data.

Both use the same parameters as standard CSV import.

---

## Unemployment Analysis

Specialized analysis endpoints for unemployment inequality assessment.

### 1. Regional Gap Analysis
**GET** `/analysis/unemployment/regional-gap/{year}`

Comprehensive regional gap analysis for unemployment rates.

**Path Parameters:**
| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| year | integer | 2020-2030 | Year to analyze |

**Response (200):**
```json
{
  "year": 2023,
  "national_rate": 5.2,
  "gap_index": 0.452,
  "provinces": [
    {
      "region_code": "31",
      "provinsi": "DKI Jakarta",
      "unemployment_rate": 3.8,
      "score": 78.5,
      "ranking": 1,
      "severity": "low",
      "trend": "improving"
    }
  ],
  "alerts": [
    {
      "region_code": "53",
      "provinsi": "Nusa Tenggara Timur",
      "severity": "critical",
      "message": "Unemployment rate critically high"
    }
  ]
}
```

**Error Responses:**
- **404:** Data not available for year

---

### 2. Year Comparison
**GET** `/analysis/unemployment/compare`

Year-over-year comparison analysis.

**Query Parameters:**
| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| year_from | integer | Yes | 2020-2030 | Starting year |
| year_to | integer | Yes | 2020-2030 | Ending year |

**Constraint:** `year_from` must be less than `year_to`

**Response (200):**
```json
{
  "year_from": 2022,
  "year_to": 2023,
  "improved": 15,
  "worsened": 12,
  "stable": 11,
  "biggest_improvement": {
    "region_code": "31",
    "change": -1.5
  },
  "biggest_decline": {
    "region_code": "53",
    "change": 2.3
  },
  "provincial_trends": [
    {
      "region_code": "31",
      "rate_2022": 5.0,
      "rate_2023": 3.8,
      "change": -1.2,
      "status": "improved"
    }
  ]
}
```

**Error Responses:**
- **400:** Invalid year range

---

### 3. Critical Alerts
**GET** `/analysis/unemployment/alerts/{year}`

Get only provinces with critical or high severity alerts.

**Path Parameters:**
| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| year | integer | 2020-2030 | Year to check |

**Response (200):**
```json
{
  "year": 2023,
  "critical_count": 2,
  "high_count": 5,
  "alerts": [
    {
      "region_code": "53",
      "provinsi": "Nusa Tenggara Timur",
      "severity": "critical",
      "unemployment_rate": 12.5,
      "reason": "Rate exceeds national average by 240%"
    }
  ]
}
```

---

## Error Handling

### Standard Error Response Format

All errors follow a consistent response format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Delete successful (no response body) |
| 400 | Bad Request | Invalid query parameters or malformed request body |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists or duplicate key violation |
| 500 | Internal Server Error | Unexpected server error |

### Common Error Responses

**400 - Bad Request:**
```json
{
  "detail": "File must be a CSV"
}
```

**404 - Not Found:**
```json
{
  "detail": "Region with code '99' not found"
}
```

**409 - Conflict:**
```json
{
  "detail": "Data for province_id '31' and tahun 2023 already exists"
}
```

### Validation Errors

When validation fails, the response includes detailed field errors:

```json
{
  "detail": [
    {
      "loc": ["body", "value"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Pagination

Most list endpoints support pagination using `skip` and `limit` or `page` and `page_size` parameters.

### Skip/Limit Pattern (Used in most endpoints)
```
GET /api/v1/indicators?skip=0&limit=50
```

### Page/Page_Size Pattern (Used in region endpoints)
```
GET /api/v1/regions?page=1&page_size=20
```

### Paginated Response Format
```json
{
  "items": [...],
  "total": 456,
  "skip": 0,
  "limit": 50
}
```

or

```json
{
  "regions": [...],
  "total": 38,
  "page": 1,
  "page_size": 20
}
```

---

## Authentication

Currently, the API has **no authentication** implemented. All endpoints are public.

For future implementation, authorization should be added at the API Gateway or middleware level.

---

## CORS Configuration

The API supports Cross-Origin Resource Sharing (CORS) for frontend access.

**Allowed Origins:** Configured in environment variables  
**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS  
**Allowed Headers:** All  
**Credentials:** Allowed

---

## Rate Limiting

Currently, the API has **no rate limiting** implemented.

For production deployment, rate limiting should be implemented to prevent abuse.

Suggested limits:
- 1000 requests per minute per IP
- 10000 requests per day per IP

---

## API Documentation

### Interactive Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

These auto-generated documentation pages are based on OpenAPI 3.0 specification and can be used to:
- Explore all available endpoints
- Test API calls directly
- View detailed parameter documentation
- Download API schema

---

## Code Examples

### cURL

```bash
# List regions
curl -X GET "http://localhost:8000/api/v1/regions?page=1&page_size=10"

# Get regional rankings
curl -X GET "http://localhost:8000/scores/rankings?year=2023"

# Import CSV data
curl -X POST "http://localhost:8000/api/v1/gini-ratio/import-csv" \
  -F "file=@data.csv" \
  -F "tahun=2023"

# Update configuration
curl -X PUT "http://localhost:8000/configs/weights/indicators" \
  -H "Content-Type: application/json" \
  -d '{"HDI": 0.30, "POVERTY_RATE": 0.25, ...}'
```

### JavaScript/Fetch

```javascript
// List regions
const response = await fetch('http://localhost:8000/api/v1/regions?page=1&page_size=10');
const data = await response.json();
console.log(data.regions);

// Get regional rankings
const rankings = await fetch('http://localhost:8000/scores/rankings?year=2023');
const rankData = await rankings.json();
console.log(rankData.rankings);

// Create region
const createResponse = await fetch('http://localhost:8000/api/v1/regions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: '31',
    properties: {
      KODE_PROV: '31',
      PROVINSI: 'DKI Jakarta'
    }
  })
});
const result = await createResponse.json();
console.log(result.message);
```

### Python

```python
import requests

# List regions
response = requests.get('http://localhost:8000/api/v1/regions', params={'page': 1, 'page_size': 10})
data = response.json()
print(data['regions'])

# Get regional rankings
rankings = requests.get('http://localhost:8000/scores/rankings', params={'year': 2023})
print(rankings.json()['rankings'])

# Create region
region = {
    'id': '31',
    'properties': {
        'KODE_PROV': '31',
        'PROVINSI': 'DKI Jakarta'
    }
}
response = requests.post('http://localhost:8000/api/v1/regions', json=region)
print(response.json()['message'])
```

---

## Best Practices

### Request/Response Handling

1. **Always check HTTP status codes** - Don't assume all successful responses return 200
2. **Handle 404 errors** - Resources may not exist even if the endpoint is valid
3. **Validate input** - Client-side validation improves UX before sending requests
4. **Implement retry logic** - For transient failures (500, 503)
5. **Use pagination** - Never fetch all records without pagination

### Performance Tips

1. **Filter early** - Use query parameters to reduce result set
2. **Limit pagination** - Use reasonable page_size (20-50 recommended)
3. **Cache responses** - Geographic data and configuration change rarely
4. **Batch operations** - Use `/imports/batch` for multiple inserts instead of individual POSTs
5. **Use appropriate endpoints** - Use `/scores/top-bottom` instead of `/scores` + client-side filtering

### Security Considerations

1. **Validate file uploads** - Check file type and size
2. **Sanitize user input** - Especially for search/filter parameters
3. **Handle sensitive data** - Don't log personal information
4. **Use HTTPS** - Always use HTTPS in production
5. **Implement authentication** - Before production deployment

---

## Troubleshooting

### Common Issues

**Issue:** "Region not found" when querying  
**Solution:** Verify region code format. Should be KODE_PROV (e.g., "31" not "ID-JK")

**Issue:** 409 Conflict on import  
**Solution:** Data already exists for that province/year combination. Use PUT to update instead.

**Issue:** Empty results from /scores endpoints  
**Solution:** Ensure scores have been calculated. Run POST `/scores/recalculate` first.

**Issue:** Import fails with malformed CSV error  
**Solution:** Verify CSV format matches expected structure. Use POST `/imports/validate` first.

---

## Support & Documentation

For additional help:
- Check the [API Documentation](./api-contract.md)
- Review [Data Sources](./data-sources.md)
- See [Scoring Method](./scoring-method.md)
- Check [Architecture](./architecture.md)

---

**Last Updated:** January 15, 2025  
**Maintained By:** Regional Gap Analyzer Development Team
