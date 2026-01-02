# Geographic Data

This folder contains GeoJSON boundary files for Indonesian provinces.

## Files

### indonesia_provinces.geojson

GeoJSON FeatureCollection containing boundaries for all 38 provinces of Indonesia.

**Source:** [TODO - Add official source]
- Original download: Badan Informasi Geospasial (BIG) or other authoritative source
- Download date: [TODO]
- Projection: WGS84 (EPSG:4326)

## Province Code Mapping

The `properties.code` field uses ISO 3166-2:ID codes. Mapping to BPS codes:

| ISO Code | BPS Code | Province Name |
|----------|----------|---------------|
| ID-AC | 11 | Aceh |
| ID-SU | 12 | Sumatera Utara |
| ID-SB | 13 | Sumatera Barat |
| ID-RI | 14 | Riau |
| ID-JA | 15 | Jambi |
| ID-SS | 16 | Sumatera Selatan |
| ID-BE | 17 | Bengkulu |
| ID-LA | 18 | Lampung |
| ID-BB | 19 | Kepulauan Bangka Belitung |
| ID-KR | 21 | Kepulauan Riau |
| ID-JK | 31 | DKI Jakarta |
| ID-JB | 32 | Jawa Barat |
| ID-JT | 33 | Jawa Tengah |
| ID-YO | 34 | DI Yogyakarta |
| ID-JI | 35 | Jawa Timur |
| ID-BT | 36 | Banten |
| ID-BA | 51 | Bali |
| ID-NB | 52 | Nusa Tenggara Barat |
| ID-NT | 53 | Nusa Tenggara Timur |
| ID-KB | 61 | Kalimantan Barat |
| ID-KT | 62 | Kalimantan Tengah |
| ID-KS | 63 | Kalimantan Selatan |
| ID-KI | 64 | Kalimantan Timur |
| ID-KU | 65 | Kalimantan Utara |
| ID-SA | 71 | Sulawesi Utara |
| ID-ST | 72 | Sulawesi Tengah |
| ID-SN | 73 | Sulawesi Selatan |
| ID-SG | 74 | Sulawesi Tenggara |
| ID-GO | 75 | Gorontalo |
| ID-SR | 76 | Sulawesi Barat |
| ID-MA | 81 | Maluku |
| ID-MU | 82 | Maluku Utara |
| ID-PB | 91 | Papua Barat |
| ID-PA | 94 | Papua |
| ID-PD | 92 | Papua Barat Daya |
| ID-PS | 93 | Papua Selatan |
| ID-PT | 95 | Papua Tengah |
| ID-PE | 96 | Papua Pegunungan |

## GeoJSON Structure

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "code": "ID-JK",
        "name": "DKI Jakarta",
        "bps_code": "31"
      },
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [...]
      }
    }
  ]
}
```

## Usage Notes

1. **Simplification**: For web performance, boundaries may be simplified using tools like mapshaper
2. **Updates**: Province boundaries should be updated when administrative changes occur
3. **Attribution**: Include proper attribution when displaying maps

## TODO

- [ ] Download official boundaries from BIG
- [ ] Validate all province codes match
- [ ] Simplify for web use (target <2MB)
- [ ] Add centroid coordinates for labels
