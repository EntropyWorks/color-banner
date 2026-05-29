# Banner Scripts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `make banners` target that generates 9 self-contained CI notification scripts into `assets/bin/`, then wire those scripts into the CI and publish workflows.

**Architecture:** `make banners` calls `color-banner --export` nine times to produce standalone bash scripts with base64-encoded ANSI banners. The generated scripts are committed to the repo and called directly in GitHub Actions steps with `if: success()` / `if: failure()` guards.

**Tech Stack:** GNU Make, uv, color-banner CLI, GitHub Actions, bash

**Branch:** `dog-food` (merge to `main` when complete)

---

## File Map

| Action | Path |
|--------|------|
| Modify | `Makefile` |
| Create (×9) | `assets/bin/tests-passed.sh`, `assets/bin/build-complete.sh`, `assets/bin/published.sh`, `assets/bin/deployed.sh`, `assets/bin/tests-skipped.sh`, `assets/bin/build-warning.sh`, `assets/bin/tests-failed.sh`, `assets/bin/build-failed.sh`, `assets/bin/deploy-failed.sh` |
| Modify | `.github/workflows/ci.yml` |
| Modify | `.github/workflows/publish.yml` |

---

## Task 1: Add `banners` target to Makefile

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Add `BANNER_FONT` variable and `banners` to `.PHONY`**

Replace the top of `Makefile` (lines 1–3) so it reads:

```makefile
PYTHON_VERSIONS := 3.11 3.12 3.13
BANNER_FONT     := slant

.PHONY: test test-quick clean banners
```

- [ ] **Step 2: Add `banners` target after `test-quick` and before `clean`**

Insert this block between the `test-quick` target and the `## clean:` line. Use real tabs (not spaces) for indentation — Make requires tabs:

```makefile
## banners: generate self-contained banner scripts into assets/bin/
banners:
	@mkdir -p assets/bin
	@uv run color-banner "Tests Passed"    --palette ocean  --font $(BANNER_FONT) --export assets/bin/tests-passed.sh
	@uv run color-banner "Build Complete"  --palette ocean  --font $(BANNER_FONT) --export assets/bin/build-complete.sh
	@uv run color-banner "Published"       --palette ocean  --font $(BANNER_FONT) --export assets/bin/published.sh
	@uv run color-banner "Deployed"        --palette ocean  --font $(BANNER_FONT) --export assets/bin/deployed.sh
	@uv run color-banner "Tests Skipped"   --palette sunset --font $(BANNER_FONT) --export assets/bin/tests-skipped.sh
	@uv run color-banner "Build Warning"   --palette sunset --font $(BANNER_FONT) --export assets/bin/build-warning.sh
	@uv run color-banner "Tests Failed"    --palette fire   --font $(BANNER_FONT) --export assets/bin/tests-failed.sh
	@uv run color-banner "Build Failed"    --palette fire   --font $(BANNER_FONT) --export assets/bin/build-failed.sh
	@uv run color-banner "Deploy Failed"   --palette fire   --font $(BANNER_FONT) --export assets/bin/deploy-failed.sh
	@echo "Generated assets/bin/ with font: $(BANNER_FONT)"
```

- [ ] **Step 3: Verify `make help` shows the new target**

```bash
make help
```

Expected output includes:
```
  banners: generate self-contained banner scripts into assets/bin/
```

- [ ] **Step 4: Commit**

```bash
git add Makefile
git commit -m "build: add banners Makefile target with configurable BANNER_FONT"
```

---

## Task 2: Generate the 9 banner scripts

**Files:**
- Create: `assets/bin/*.sh` (9 files)

- [ ] **Step 1: Run the banners target**

```bash
make banners
```

Expected output:
```
Generated assets/bin/ with font: slant
```

- [ ] **Step 2: Verify all 9 files were created**

```bash
ls assets/bin/
```

Expected output:
```
build-complete.sh  build-failed.sh  build-warning.sh  deploy-failed.sh  deployed.sh
published.sh  tests-failed.sh  tests-passed.sh  tests-skipped.sh
```

- [ ] **Step 3: Validate each script is valid bash**

```bash
for f in assets/bin/*.sh; do bash -n "$f" && echo "OK: $f"; done
```

Expected: 9 lines all reading `OK: assets/bin/<name>.sh`

- [ ] **Step 4: Spot-check a success script contains base64 content and an ocean palette colour**

```bash
grep -c "base64" assets/bin/tests-passed.sh
grep "38;2;" assets/bin/tests-passed.sh | head -1 | cut -c1-40
```

Expected: first command prints `1`; second prints a line starting with `printf '%s'`

- [ ] **Step 5: Spot-check a failure script contains fire palette (red tones — high R, low G/B)**

```bash
grep "38;2;" assets/bin/tests-failed.sh | head -1 | cut -c1-60
```

Expected: a line containing `\x1b[38;2;` ANSI codes (red-range values).

- [ ] **Step 6: Run one script end-to-end to confirm it prints output**

```bash
bash assets/bin/tests-passed.sh | wc -l
```

Expected: a number greater than 0 (banner has multiple lines).

- [ ] **Step 7: Commit**

```bash
git add assets/bin/
git commit -m "feat: add pre-generated CI banner scripts (slant font)"
```

---

## Task 3: Wire banner steps into ci.yml

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Add banner steps after `Run tests`**

The current `ci.yml` test job ends at the `Run tests` step. Add two steps immediately after it:

```yaml
name: CI

on:
  push:
  pull_request:
    branches: ["main"]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --group dev

      - name: Run tests
        run: uv run pytest tests/ -v

      - name: Banner — success
        if: success()
        run: bash assets/bin/tests-passed.sh

      - name: Banner — failure
        if: failure()
        run: bash assets/bin/tests-failed.sh
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: show banner after test job (success=ocean, failure=fire)"
```

---

## Task 4: Wire banner steps into publish.yml

**Files:**
- Modify: `.github/workflows/publish.yml`

- [ ] **Step 1: Add banner steps to the `publish` job after `Publish to PyPI`**

The current `publish` job ends at `Publish to PyPI`. Add two steps immediately after it:

```yaml
name: Publish to PyPI

on:
  workflow_run:
    workflows: ["Release Please"]
    types: [completed]
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    if: >
      github.event_name == 'workflow_dispatch' ||
      (github.event.workflow_run.conclusion == 'success' &&
       startsWith(github.event.workflow_run.head_commit.message, 'chore(main): release'))
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha || github.sha }}

      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: uv sync --group dev

      - name: Run tests
        run: uv run pytest tests/ -v

  publish:
    needs: test
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha || github.sha }}

      - uses: astral-sh/setup-uv@v5

      - name: Build
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

      - name: Banner — published
        if: success()
        run: bash assets/bin/published.sh

      - name: Banner — failure
        if: failure()
        run: bash assets/bin/build-failed.sh
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml')); print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "ci: show banner after publish job (success=published, failure=build-failed)"
```

---

## Task 5: Verify and push

- [ ] **Step 1: Confirm all expected files are present**

```bash
ls assets/bin/
git log --oneline -5
```

Expected `assets/bin/` contents (9 files):
```
build-complete.sh  build-failed.sh  build-warning.sh  deploy-failed.sh  deployed.sh
published.sh  tests-failed.sh  tests-passed.sh  tests-skipped.sh
```

Expected log (most recent first):
```
<hash> ci: show banner after publish job (success=published, failure=build-failed)
<hash> ci: show banner after test job (success=ocean, failure=fire)
<hash> feat: add pre-generated CI banner scripts (slant font)
<hash> build: add banners Makefile target with configurable BANNER_FONT
```

- [ ] **Step 2: Run a quick test to confirm nothing broke**

```bash
make test-quick
```

Expected: all tests pass.

- [ ] **Step 3: Push the branch**

```bash
git push origin dog-food
```

After pushing, open a PR from `dog-food` → `main` on GitHub.
