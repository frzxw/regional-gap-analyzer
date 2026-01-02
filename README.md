# Regional Gap Analyzer

Regional Inequality Analysis System — Province-level scoring and geospatial heatmap visualization.

## 🏗️ Project Structure

```
regional-gap-analyzer/
├── backend/           # FastAPI + MongoDB backend
├── frontend/          # Next.js App Router frontend
├── data/              # Raw, processed, and geo data
├── docs/              # Project documentation
├── docker-compose.yml # Container orchestration
└── .github/           # CI/CD and PR templates
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js >= 18 (for local dev)
- Python >= 3.11 (for local dev)

### Run with Docker

```bash
# Clone and enter the repo
cd regional-gap-analyzer

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Start all services
docker compose up --build

# Verify backend health
curl http://localhost:8000/health

# Open frontend dashboard
# http://localhost:3000/dashboard
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🌿 Branching Workflow

This project uses a **trunk-based development** workflow suitable for a 6-person team.

### Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<scope>/<short-desc>` | `feature/api/scoring-endpoint` |
| Bug Fix | `fix/<scope>/<short-desc>` | `fix/web/map-zoom-issue` |
| Chore | `chore/<scope>/<short-desc>` | `chore/infra/update-deps` |

**Scopes:** `api`, `web`, `data`, `docs`, `infra`

### Creating a Feature Branch

```bash
# Ensure you're on latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/api/my-new-feature

# Make changes, commit, push
git add .
git commit -m "feat(api): add new endpoint for X"
git push -u origin feature/api/my-new-feature

# Create a Pull Request on GitHub
# After approval and CI pass, squash merge to main
```

### Protected Branches
- `main` — Always stable, demo-ready
- `release/demo` — Optional freeze branch for demo week

See [docs/branching.md](docs/branching.md) for full details.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Branching Model](docs/branching.md)
- [API Contract](docs/api-contract.md)
- [Data Sources](docs/data-sources.md)
- [Scoring Method](docs/scoring-method.md)
- [Demo Script](docs/demo-script.md)

## 🧪 Testing

```bash
# Backend tests (TODO)
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
