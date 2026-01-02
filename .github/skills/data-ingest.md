# Skill: Data Ingest & Validation

Data ingest rules:
- All ingested data must come from documented sources
- Raw files are stored under /data/raw
- Transformed files go to /data/processed
- Every import creates an import_batch record

Validation requirements:
- schema validation
- missing value detection
- outlier detection (no deletion without justification)

Never auto-fix data silently.
