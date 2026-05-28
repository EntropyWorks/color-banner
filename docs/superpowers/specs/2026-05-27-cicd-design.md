# CI/CD Design — color-banner

## Overview

Three GitHub Actions workflow files, each with one responsibility. The pipeline
separates continuous integration (always runs) from release management (on main)
and publishing (on GitHub Release).

### Flow

```
feat: commit → merge to main
  → ci.yml runs tests (passes)
  → release-please.yml opens/updates "chore(main): release X.Y.Z" PR
  → you merge the Release PR
  → release-please creates GitHub Release + tag
  → publish.yml fires → re-runs tests → publishes to PyPI
```

---

## Workflow 1 — `ci.yml`

**Triggers:** `push` to any branch, `pull_request` targeting `main`

**Jobs:**

- `test` — matrix over Python 3.11, 3.12, 3.13 on `ubuntu-latest`
  - Steps: `actions/checkout@v4` → `astral-sh/setup-uv@v5` → `uv sync --group dev` → `uv run pytest tests/ -v`

**Notes:**
- No code quality checks (linting, type checking) — tests only
- No coverage reporting

---

## Workflow 2 — `release-please.yml`

**Triggers:** `push` to `main`

**Jobs:**

- `release-please` — runs `googleapis/release-please-action@v4`
  - Package type: `python`
  - Reads conventional commits to determine version bump:
    - `fix:` → patch (0.1.0 → 0.1.1)
    - `feat:` → minor (0.1.0 → 0.2.0)
    - `feat!:` or `BREAKING CHANGE:` → major (0.1.0 → 1.0.0)
  - Opens/updates a PR titled `chore(main): release X.Y.Z`
  - Bumps `version` in `pyproject.toml` automatically
  - When Release PR is merged: creates GitHub Release + tag (e.g. `v0.2.0`)

**Permissions required:** `contents: write`, `pull-requests: write`

**Config files (committed to repo):**

`.github/release-please-config.json`:
```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "release-type": "python",
  "packages": {
    ".": {}
  }
}
```

`.release-please-manifest.json`:
```json
{
  ".": "0.1.0"
}
```

---

## Workflow 3 — `publish.yml`

**Triggers:** `release: types: [published]`

**Jobs:**

1. `test` — re-runs tests on `ubuntu-latest` + Python 3.11 as a safety gate
   - Same steps as `ci.yml` test job (single version, not a matrix)

2. `publish` — depends on `test` passing
   - Environment: `pypi` (must match exactly — case-sensitive)
   - Permission: `id-token: write` (OIDC trusted publishing, no stored token)
   - Steps: `actions/checkout@v4` → `astral-sh/setup-uv@v5` → `uv build` → `pypa/gh-action-pypi-publish@release/v1`

**PyPI trusted publisher config** (set up on pypi.org):
- Owner: `EntropyWorks`
- Repository: `color-banner`
- Workflow: `publish.yml`
- Environment: `pypi`

---

## Dependabot

File: `.github/dependabot.yml`

- Checks for GitHub Actions version updates weekly
- Checks for Python dependency updates weekly (targets `pyproject.toml`)
- Opens PRs automatically; tests run via `ci.yml` on those PRs

---

## Files to Create

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Test matrix |
| `.github/workflows/release-please.yml` | Automated Release PR + tag |
| `.github/workflows/publish.yml` | PyPI publish on release |
| `release-please-config.json` | release-please package config |
| `.release-please-manifest.json` | Current version tracking |
| `.github/dependabot.yml` | Automatic dependency updates |

The existing `.github/workflows/publish.yml` (created earlier this session) will be replaced by the three new workflow files.
