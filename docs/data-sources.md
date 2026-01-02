# Data Sources

## Overview

This document describes the data sources used for the Regional Gap Analyzer.

**IMPORTANT:** All data currently in this repository is for demonstration purposes only. Official data must be sourced from authoritative government or international organizations.

## Potential Data Sources

### Economic Indicators

| Indicator | Potential Source | Frequency | Notes |
|-----------|------------------|-----------|-------|
| GDP per Capita | BPS (Statistics Indonesia) | Annual | By province |
| Unemployment Rate | BPS Labor Force Survey | Quarterly | |
| Poverty Rate | BPS SUSENAS | Annual | |
| Gini Coefficient | BPS | Annual | Income inequality |

### Infrastructure Indicators

| Indicator | Potential Source | Frequency | Notes |
|-----------|------------------|-----------|-------|
| Road Density | Ministry of Public Works | Annual | km per sq km |
| Electricity Access | PLN, Ministry of Energy | Annual | % households |
| Internet Penetration | APJII, Kominfo | Annual | % population |
| Clean Water Access | BPS, Ministry of Health | Annual | % households |

### Health Indicators

| Indicator | Potential Source | Frequency | Notes |
|-----------|------------------|-----------|-------|
| Hospital Beds | Ministry of Health | Annual | per 10,000 pop |
| Life Expectancy | BPS | Annual | Years |
| Infant Mortality | BPS, WHO | Annual | per 1,000 births |
| Doctor Ratio | Ministry of Health | Annual | per 10,000 pop |

### Education Indicators

| Indicator | Potential Source | Frequency | Notes |
|-----------|------------------|-----------|-------|
| Literacy Rate | BPS | Annual | % age 15+ |
| School Enrollment | Ministry of Education | Annual | Net enrollment |
| Years of Schooling | BPS | Annual | Mean years |
| Teacher-Student Ratio | Ministry of Education | Annual | |

## Geographic Data

| Data Type | Source | Format | Notes |
|-----------|--------|--------|-------|
| Province Boundaries | BIG (Geospatial Agency) | GeoJSON | Official boundaries |
| District Boundaries | BIG | GeoJSON | Kabupaten/Kota level |
| Centroids | Derived | JSON | For map markers |

## Data Collection Process

### 1. Acquisition
- Download from official sources
- Document source URL, date, and version
- Store original files in `data/raw/`

### 2. Validation
- Check for missing values
- Validate geographic codes
- Cross-reference with official region lists

### 3. Processing
- Clean and standardize formats
- Apply normalization
- Calculate derived indicators
- Store in `data/processed/`

### 4. Import
- Run data import scripts
- Verify MongoDB collections
- Update data version in metadata

## Demo Data

For development purposes, we use synthetic demo data that:
- Follows realistic distributions
- Covers all 34 provinces
- Is clearly marked as "DEMO - NOT OFFICIAL"

Demo data is generated using scripts in `backend/scripts/` (TODO).

## Data Update Schedule

| Data Type | Update Frequency | Responsibility |
|-----------|------------------|----------------|
| Economic | Quarterly | Data Team |
| Infrastructure | Annually | Data Team |
| Health | Annually | Data Team |
| Geographic | As needed | Infra Team |

## TODO

- [ ] Create data download scripts for official sources
- [ ] Implement data validation pipeline
- [ ] Set up automated data refresh schedule
- [ ] Add data versioning system
