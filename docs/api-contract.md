# API Contract

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.regional-gap-analyzer.example.com`

## Authentication

**TODO:** Implement API key authentication for production.

Currently, the API is open for development purposes.

## Endpoints

### Health Check

#### `GET /health`

Basic health check.

**Response:**
```json
{
  "status": "ok"
}
```

#### `GET /health/detailed`

Detailed health check including database status.

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### Regions

Base path: `/api/v1/regions`

#### `GET /api/v1/regions`

List all regions with pagination.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page |

**Response:**
```json
{
  "regions": [
    {
      "id": "507f1f77bcf86cd799439011",
      "code": "ID-JK",
      "name": "DKI Jakarta",
      "province": "DKI Jakarta"
    }
  ],
  "total": 34
}
```

#### `GET /api/v1/regions/{region_id}`

Get a single region by ID.

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "code": "ID-JK",
  "name": "DKI Jakarta",
  "province": "DKI Jakarta"
}
```

**Errors:**
- `404 Not Found` - Region not found

---

### Scores (TODO)

Base path: `/api/v1/scores`

#### `GET /api/v1/scores`

List scores for all regions.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `year` | int | latest | Data year |
| `category` | string | all | Filter by category |

**Response:**
```json
{
  "scores": [
    {
      "region_code": "ID-JK",
      "region_name": "DKI Jakarta",
      "year": 2024,
      "composite_score": 85.5,
      "economic_score": 90.2,
      "infrastructure_score": 88.1,
      "health_score": 82.3,
      "education_score": 78.9
    }
  ],
  "metadata": {
    "year": 2024,
    "total_regions": 34
  }
}
```

#### `GET /api/v1/scores/{region_code}`

Get detailed scores for a specific region.

#### `GET /api/v1/scores/compare`

Compare scores between regions.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `regions` | string[] | Yes | Region codes to compare |
| `year` | int | No | Data year |

---

### Geographic Data (TODO)

Base path: `/api/v1/geo`

#### `GET /api/v1/geo/boundaries`

Get GeoJSON boundaries for all regions.

#### `GET /api/v1/geo/boundaries/{region_code}`

Get GeoJSON boundary for a specific region.

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Validation Errors

```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

## Rate Limiting

**TODO:** Implement rate limiting.

Planned limits:
- 100 requests per minute per IP
- 1000 requests per hour per API key

## Versioning

The API is versioned via URL path (`/api/v1/`).

Breaking changes will increment the version number.
