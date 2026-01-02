# Copilot Instructions — Regional Gap Analyzer

## 1. Project Context (MANDATORY)

This repository implements **Regional Gap Analyzer**, an analytical system aligned with **SDG 10 (Reducing Inequalities)**.

**Scope is STRICTLY LIMITED to:**
- Country: Indonesia
- Geographic level: **PROVINCE ONLY**
- Data type: **Secondary, official, public data**
- Primary authority: **Badan Pusat Statistik (BPS)**

This is **NOT** a demo project and **NOT** a mock-data system.

---

## 2. What This System IS

- An analytical system that:
  - ingests official statistics
  - stores local copies for analysis
  - normalizes and scores inequality indicators
  - generates rankings and alerts
  - visualizes results via maps and charts

- A system designed to be:
  - robust to missing data
  - explainable (no black box logic)
  - auditable (import batches & sources tracked)

---

## 3. What This System IS NOT (STRICTLY FORBIDDEN)

Copilot MUST NOT:
- invent datasets, indicators, or APIs
- assume province-level availability without verification
- generate survey-based logic
- generate ML / prediction logic
- generate city/regency-level logic
- fabricate “typical” government tables
- guess values, columns, or schemas

If unsure → **STOP and ask for clarification**.

---

## 4. Approved Data Sources

Copilot may ONLY reference:
- Badan Pusat Statistik (BPS)
- BMKG (climate, optional)
- KLHK (environment, optional)
- BNPB (disaster data, optional)

All data must be:
- public
- verifiable
- documented in `/docs/data-sources.md`

---

## 5. Approved Core Indicators (SAFE)

Copilot may safely work with these indicators ONLY:
- Gini Ratio
- Poverty Rate (P0)
- Number of Poor Population
- Open Unemployment Rate (TPT)
- Labor Force / Employed Population
- Average Monthly Wage
- Human Development Index (HDI / IPM)
- Consumer Price Index (CPI / IHK)
- Inflation
- Population Count

Additional indicators require **explicit confirmation**.

---

## 6. Technical Stack (LOCKED)

- Backend: **Python FastAPI**
- Database: **MongoDB**
- Data processing: **Pandas / NumPy**
- Frontend: **Next.js (App Router)**
- Repository: **Single repo**

Copilot MUST follow existing folder structure.

---

## 7. Data Handling Rules

- Raw values MUST be stored in original units
- Normalization MUST be explicit (min-max or z-score)
- Missing indicators MUST be handled via weight re-normalization
- Scores MUST be reproducible
- Configuration (weights, thresholds) MUST be stored in database

---

## 8. Coding Standards

Copilot MUST:
- generate clean, readable, commented code
- separate concerns (router / service / repository)
- avoid race conditions
- avoid hidden side effects
- avoid magic numbers
- handle edge cases explicitly

Copilot MUST NOT:
- inline business logic inside routers
- hardcode weights or thresholds
- write long unstructured functions

---

## 9. Git & Branching Awareness

Copilot MUST respect:
- trunk-based workflow
- no direct changes to `main`
- feature branches per scope (`api`, `web`, `data`, `docs`)
- small, focused commits

---

## 10. Behavior on Uncertainty (CRITICAL)

If Copilot is unsure:
- it MUST say so
- it MUST NOT hallucinate
- it MUST NOT “fill in” data
- correctness > completeness

---

## 11. Default Response Style

- Conservative
- Explicit
- Evidence-oriented
- No assumptions
- No speculation

---

## 12. Acknowledgement Rule

Before generating major logic, Copilot SHOULD internally verify:
- data source validity
- geographic scope correctness
- indicator legitimacy
