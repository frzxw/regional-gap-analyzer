# Demo Script

## Overview

This document provides a script for demonstrating the Regional Gap Analyzer system.

**Duration:** 15-20 minutes

## Prerequisites

1. Docker and Docker Compose installed
2. Repository cloned locally
3. Environment files configured

## Setup (Before Demo)

```bash
# Start all services
docker compose up -d

# Verify services are running
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Open frontend
open http://localhost:3000/dashboard
```

## Demo Flow

### 1. Introduction (2 min)

**Talking Points:**
- Purpose: Analyze regional inequality at province level
- Data-driven approach to identify development gaps
- Helps policymakers prioritize resource allocation

### 2. Architecture Overview (3 min)

**Show:**
- `docs/architecture.md` diagram
- Three-tier architecture: Frontend → Backend → Database
- Clean separation of concerns

**Talking Points:**
- Next.js for modern, responsive UI
- FastAPI for high-performance API
- MongoDB for flexible data storage

### 3. API Demo (5 min)

**Actions:**

```bash
# Health check
curl http://localhost:8000/health

# Detailed health (shows DB connection)
curl http://localhost:8000/health/detailed

# API documentation
open http://localhost:8000/docs
```

**Show:**
- Swagger UI auto-generated documentation
- Try out endpoints interactively
- Response schemas

### 4. Dashboard Demo (5 min)

**Actions:**
- Navigate to http://localhost:3000/dashboard
- Show health status indicator
- (TODO) Show interactive map with region data
- (TODO) Demonstrate filtering by category
- (TODO) Show region comparison feature

**Talking Points:**
- Real-time data from backend API
- Interactive Leaflet map visualization
- Color-coded by development score

### 5. Scoring Methodology (3 min)

**Show:**
- `docs/scoring-method.md`
- Explain normalization process
- Discuss category weights

**Talking Points:**
- Multi-dimensional analysis (Economic, Infrastructure, Health, Education)
- Transparent, reproducible methodology
- Customizable weights for different policy priorities

### 6. Q&A (2 min)

**Common Questions:**
- Data sources and update frequency
- How to add new indicators
- Deployment options

## Troubleshooting

### Services not starting
```bash
docker compose down
docker compose up --build
```

### Database connection issues
```bash
# Check MongoDB is running
docker compose ps

# View backend logs
docker compose logs backend
```

### Frontend not loading
```bash
# Check frontend logs
docker compose logs frontend

# Verify backend URL
cat frontend/.env.local
```

## Post-Demo Cleanup

```bash
# Stop services
docker compose down

# Remove volumes (optional, deletes data)
docker compose down -v
```

## TODO

- [ ] Add sample data loading script
- [ ] Create pre-recorded backup video
- [ ] Add map visualization demo
- [ ] Add comparison feature demo
