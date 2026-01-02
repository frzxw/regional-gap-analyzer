# Branching Model

This document describes the Git branching strategy for the Regional Gap Analyzer project.

## Overview

We use a **Git-Flow inspired** workflow optimized for a 6-person team working in a single repository. This approach emphasizes:

- Short-lived feature branches
- Integration to `develop` (not directly to `main`)
- Protected branches with required reviews
- Automated CI checks before merge
- Periodic releases from `develop` to `main`

## Protected Branches

### `main`
- **Always stable and production-ready**
- No direct pushes allowed
- Only receives merges from `develop` or hotfix branches
- Represents the latest release

### `develop`
- **Integration branch for features**
- No direct pushes allowed
- All feature branches merge here via PR
- Requires at least 1 reviewer approval
- CI must pass before merge
- Prefer squash merge to keep history clean

### `release/demo` (optional)
- Created before demo week as a freeze branch from `develop`
- Only critical bug fixes allowed
- Merges back to both `main` and `develop` after demo

## Working Branches

### Naming Convention

```
<type>/<scope>/<short-description>
```

| Type | Use Case |
|------|----------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `chore/` | Maintenance, refactoring, deps |

| Scope | Description |
|-------|-------------|
| `api` | Backend API changes |
| `web` | Frontend changes |
| `data` | Data processing, ingestion |
| `docs` | Documentation |
| `infra` | CI/CD, Docker, deployment |

### Examples

```bash
feature/api/scoring-endpoint
feature/web/heatmap-component
feature/data/gdp-normalization
fix/api/cors-headers
fix/web/map-zoom-reset
chore/infra/update-python-deps
chore/docs/api-contract-update
```

## Workflow

### 1. Start a New Feature

```bash
# Ensure you're on latest develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/api/my-new-feature
```

### 2. Make Changes and Commit

```bash
# Make your changes
git add .
git commit -m "feat(api): add endpoint for region scoring"

# Push to remote
git push -u origin feature/api/my-new-feature
```

### 3. Create Pull Request

1. Go to GitHub and create a Pull Request **targeting `develop`**
2. Fill in the PR template
3. Request review from at least 1 team member
4. Ensure CI passes

### 4. Review and Merge

1. Address reviewer feedback
2. Once approved and CI passes, **squash merge** to `develop`
3. Delete the feature branch

```bash
# If merging locally (simulating PR merge)
git checkout develop
git merge --squash feature/api/my-new-feature
git commit -m "feat(api): add endpoint for region scoring (#123)"
git push origin develop

# Delete branch
git branch -d feature/api/my-new-feature
git push origin --delete feature/api/my-new-feature
```

### 5. Release to Main (Periodic)

When `develop` is stable and ready for release:

```bash
git checkout main
git merge develop
git push origin main
```

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```
feat(api): add GET /regions endpoint
fix(web): resolve map zoom issue on mobile
docs(api): update API contract for scoring
chore(infra): upgrade FastAPI to 0.109.0
```

## Branch Protection Rules (GitHub Settings)

Configure these rules for `main`:

1. **Require pull request reviews before merging**
   - Required approving reviews: 1
   - Dismiss stale reviews when new commits are pushed

2. **Require status checks to pass before merging**
   - Require branches to be up to date before merging
   - Status checks: `ci` (from GitHub Actions)

3. **Require conversation resolution before merging**

4. **Do not allow bypassing the above settings**

5. **Restrict who can push to matching branches**
   - Only allow merges via PR

## Best Practices

1. **Keep branches short-lived** (1-2 days max)
2. **Pull from main frequently** to reduce merge conflicts
3. **Write descriptive PR titles** and descriptions
4. **Review PRs promptly** (within 24 hours)
5. **Use draft PRs** for work-in-progress
6. **Squash commits** to keep main history clean
7. **Delete branches** after merging

## Team Members and Scopes

| Member | Primary Scope |
|--------|---------------|
| Dev 1 | `api` (Backend) |
| Dev 2 | `api` (Backend) |
| Dev 3 | `web` (Frontend) |
| Dev 4 | `web` (Frontend) |
| Dev 5 | `data` (Data Processing) |
| Dev 6 | `infra` + `docs` |

## Emergency Hotfix Process

For critical production issues:

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b fix/api/critical-bug

# Fix, commit, push
git commit -m "fix(api): critical security patch"
git push -u origin fix/api/critical-bug

# Fast-track PR review (still requires 1 approval)
# Merge immediately after approval
```
