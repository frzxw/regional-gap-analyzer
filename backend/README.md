# Regional Gap Analyzer - Backend

FastAPI backend for the Regional Inequality Analysis System.

## Architecture

```
app/
├── main.py          # FastAPI application factory
├── settings.py      # Configuration management
├── logging.py       # Logging configuration
├── db/              # Database connection and indexes
├── common/          # Shared utilities (errors, pagination, time)
├── models/          # Pydantic models
├── repositories/    # Data access layer
├── services/        # Business logic layer
├── routers/         # API endpoints
├── pipelines/       # Data processing pipelines
│   ├── ingest/      # Data ingestion from various sources
│   ├── transform/   # Data transformation and normalization
│   └── validate/    # Schema and quality validation
└── tasks/           # Background tasks (score recomputation)
```

## Getting Started

### Prerequisites

- Python 3.11+
- MongoDB 7.0+

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export MONGODB_URI="mongodb://localhost:27017"
export DATABASE_NAME="regional_gap_dev"
```

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
docker-compose up -d backend
```

## API Endpoints

### Health
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health with dependencies
- `GET /health/full` - Full system diagnostics

### Regions
- `GET /regions` - List all regions
- `GET /regions/{code}` - Get region details
- `GET /regions/{code}/indicators` - Get region indicators

### Indicators
- `GET /indicators` - List indicators with filters
- `GET /indicators/definitions` - Indicator definitions
- `GET /indicators/region/{code}` - Region indicators
- `POST /indicators` - Create indicator

### Scores
- `GET /scores` - List scores
- `GET /scores/rankings` - Get rankings
- `GET /scores/gap-analysis` - Gap analysis
- `POST /scores/recalculate` - Trigger recalculation

### Alerts
- `GET /alerts` - List alerts
- `GET /alerts/active` - Active alerts
- `POST /alerts/{id}/acknowledge` - Acknowledge alert
- `POST /alerts/generate` - Generate alerts

### Geographic
- `GET /geo/provinces` - Province GeoJSON
- `GET /geo/choropleth` - Choropleth data
- `GET /geo/province/{code}` - Single province

### Data Import
- `POST /imports/file` - Upload and import file
- `POST /imports/validate` - Validate file
- `POST /imports/batch` - Batch import

### Configuration
- `GET /configs` - List configs
- `GET /configs/weights/indicators` - Indicator weights
- `PUT /configs/weights/indicators` - Update weights

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

## Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy app/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `regional_gap_dev` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `API_PREFIX` | API route prefix | `/api/v1` |
