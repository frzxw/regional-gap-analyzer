# Skill: Data Modeling (MongoDB)

You are modeling analytical data, NOT transactional data.

Rules:
- Prefer fewer, correct fields
- Allow partial documents
- Never assume indicator completeness
- Use snake_case
- Always include time dimension

Required collections:
- regions
- sources
- import_batches
- indicator_records
- scoring_configs
- scores
- alerts

Never invent collections or fields.
