# Data Dictionary

This document defines all data fields, their types, units, and descriptions used in the Regional Gap Analyzer.

## Core Collections

### regions

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `code` | string | - | ISO 3166-2 province code (e.g., "ID-JK") |
| `name` | string | - | Official province name |
| `alt_names` | string[] | - | Alternative names/spellings |
| `bps_code` | string | - | BPS (Statistics Indonesia) code |
| `population` | integer | persons | Latest population count |
| `area_km2` | float | km² | Total area |
| `created_at` | datetime | UTC | Record creation timestamp |
| `updated_at` | datetime | UTC | Last update timestamp |

### indicators

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `id` | ObjectId | - | Unique identifier |
| `region_code` | string | - | Reference to region |
| `category` | string | - | One of: economic, infrastructure, health, education |
| `indicator_key` | string | - | Indicator identifier (e.g., "gdp_per_capita") |
| `value` | float | varies | Raw indicator value |
| `unit` | string | - | Unit of measurement |
| `year` | integer | - | Data year |
| `source_id` | ObjectId | - | Reference to data source |
| `created_at` | datetime | UTC | Record creation timestamp |

### scores

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `id` | ObjectId | - | Unique identifier |
| `region_code` | string | - | Reference to region |
| `year` | integer | - | Scoring year |
| `economic_score` | float | 0-100 | Normalized economic score |
| `infrastructure_score` | float | 0-100 | Normalized infrastructure score |
| `health_score` | float | 0-100 | Normalized health score |
| `education_score` | float | 0-100 | Normalized education score |
| `composite_score` | float | 0-100 | Weighted composite score |
| `rank` | integer | - | National ranking (1 = best) |
| `rank_delta` | integer | - | Change from previous period |
| `computed_at` | datetime | UTC | Computation timestamp |

### alerts

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `id` | ObjectId | - | Unique identifier |
| `region_code` | string | - | Reference to region |
| `alert_type` | string | - | Type: threshold, trend, anomaly |
| `severity` | string | - | Level: low, medium, high, critical |
| `indicator_key` | string | - | Related indicator |
| `message` | string | - | Human-readable description |
| `status` | string | - | Status: open, acknowledged, resolved |
| `created_at` | datetime | UTC | Alert generation time |
| `resolved_at` | datetime | UTC | Resolution time (if resolved) |

### sources

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `id` | ObjectId | - | Unique identifier |
| `name` | string | - | Source name (e.g., "BPS SUSENAS 2024") |
| `url` | string | - | Download URL |
| `download_date` | date | - | Date data was downloaded |
| `coverage_years` | integer[] | - | Years covered by this source |
| `indicators` | string[] | - | Indicator keys from this source |
| `notes` | string | - | Additional notes |

### configs

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `key` | string | - | Configuration key |
| `value` | any | - | Configuration value |
| `category_weights` | object | - | Weights for scoring categories |
| `indicator_weights` | object | - | Weights per indicator |
| `thresholds` | object | - | Alert threshold definitions |
| `updated_at` | datetime | UTC | Last update timestamp |

## Indicator Keys

### Economic Indicators

| Key | Description | Unit | Higher is Better |
|-----|-------------|------|------------------|
| `gdp_per_capita` | GDP per capita | IDR million | ✓ |
| `unemployment_rate` | Unemployment rate | % | ✗ |
| `poverty_rate` | Poverty rate | % | ✗ |
| `gini_coefficient` | Income inequality (Gini) | 0-1 | ✗ |
| `labor_participation` | Labor force participation | % | ✓ |

### Infrastructure Indicators

| Key | Description | Unit | Higher is Better |
|-----|-------------|------|------------------|
| `road_density` | Road length per area | km/km² | ✓ |
| `electricity_access` | Household electricity access | % | ✓ |
| `clean_water_access` | Household clean water access | % | ✓ |
| `internet_penetration` | Internet users | % population | ✓ |
| `sanitation_access` | Proper sanitation access | % | ✓ |

### Health Indicators

| Key | Description | Unit | Higher is Better |
|-----|-------------|------|------------------|
| `life_expectancy` | Life expectancy at birth | years | ✓ |
| `infant_mortality` | Infant mortality rate | per 1,000 | ✗ |
| `hospital_beds` | Hospital beds | per 10,000 pop | ✓ |
| `doctors_ratio` | Doctors | per 10,000 pop | ✓ |
| `stunting_rate` | Child stunting rate | % | ✗ |

### Education Indicators

| Key | Description | Unit | Higher is Better |
|-----|-------------|------|------------------|
| `literacy_rate` | Adult literacy rate | % | ✓ |
| `mean_schooling_years` | Mean years of schooling | years | ✓ |
| `net_enrollment_primary` | Primary net enrollment | % | ✓ |
| `net_enrollment_secondary` | Secondary net enrollment | % | ✓ |
| `teacher_student_ratio` | Teachers per students | ratio | ✓ |

## Notes

- All datetime fields are stored in UTC
- Scores are normalized to 0-100 scale using min-max normalization
- Inverse indicators (where lower is better) are inverted before scoring
- Missing values are handled according to `scoring-method.md`
