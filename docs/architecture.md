# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Next.js Frontend (port 3000)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Dashboard   │  │   Heatmap    │  │   Region Details     │  │
│  │     Page      │  │  Component   │  │      Page            │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                              │                                   │
│                    Leaflet Map + Charts                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (port 8000)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                        Routers                            │  │
│  │   /health  │  /api/v1/regions  │  /api/v1/scores         │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │                       Services                            │  │
│  │   RegionService  │  ScoringService  │  DataIngestService │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────▼───────────────────────────────┐  │
│  │                     Repositories                          │  │
│  │   RegionRepository  │  ScoreRepository                    │  │
│  └──────────────────────────┬───────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MongoDB (port 27017)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   regions    │  │    scores    │  │      geo_features    │  │
│  │  collection  │  │  collection  │  │      collection      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Architecture (Clean Architecture)

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── settings.py          # Configuration management
│   │
│   ├── routers/             # HTTP layer - request/response handling
│   │   ├── health.py
│   │   └── regions.py
│   │
│   ├── services/            # Business logic layer
│   │   ├── region_service.py
│   │   └── scoring_service.py
│   │
│   ├── repositories/        # Data access layer
│   │   └── region_repository.py
│   │
│   ├── models/              # Pydantic models / schemas
│   │   └── region.py
│   │
│   └── db/                  # Database connection
│       └── client.py
│
├── requirements.txt
└── Dockerfile
```

### Layer Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Routers** | HTTP request handling, validation, response formatting |
| **Services** | Business logic, orchestration, data transformation |
| **Repositories** | Database operations, query building |
| **Models** | Data schemas, validation rules |
| **DB** | Connection management |

### Dependency Flow

```
Routers → Services → Repositories → DB
              ↓
           Models
```

## Frontend Architecture

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   └── dashboard/       # Dashboard feature
│   │       └── page.tsx
│   │
│   ├── components/          # Reusable UI components
│   │   └── map/             # Map-related components
│   │
│   ├── lib/                 # Utilities and helpers
│   │   └── api.ts           # API client
│   │
│   └── types/               # TypeScript types
│
└── public/                  # Static assets
```

## Data Flow

### 1. Data Ingestion
```
Raw Data (CSV/JSON) → Data Processing Scripts → MongoDB
```

### 2. Scoring Calculation
```
Raw Indicators → Normalization (0-100) → Weighted Composite → Store
```

### 3. Visualization
```
API Request → MongoDB Query → Transform → JSON Response → Map/Chart Render
```

## Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Backend | FastAPI | Async support, automatic docs, type hints |
| Database | MongoDB | Flexible schema, geo queries, JSON-native |
| DB Driver | Motor | Async MongoDB driver for Python |
| Frontend | Next.js | SSR, App Router, React ecosystem |
| Maps | Leaflet | Lightweight, open-source, flexible |
| Styling | Tailwind CSS | Utility-first, rapid development |

## TODO

- [ ] Add caching layer (Redis) for frequently accessed data
- [ ] Implement WebSocket for real-time updates
- [ ] Add authentication/authorization
- [ ] Set up monitoring and logging (Prometheus, Grafana)
