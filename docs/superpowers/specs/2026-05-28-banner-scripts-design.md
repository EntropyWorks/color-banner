# Banner Scripts Design

## Overview

Generate 9 self-contained shell scripts via `color-banner --export` and commit
them to `assets/bin/`. Each script is a standalone bash function with the ANSI
banner base64-encoded inline — no `color-banner` installation required at
runtime, only `base64` (standard on all Linux/macOS). Scripts are used both as
copy-paste showcase examples and as CI pipeline notifications.

---

## Scripts

All scripts live in `assets/bin/`. Each contains a single function and calls it
immediately, so `bash assets/bin/tests-passed.sh` just works.

| File | Message | Palette | Use |
|------|---------|---------|-----|
| `tests-passed.sh` | Tests Passed | ocean | CI test job success |
| `build-complete.sh` | Build Complete | ocean | CI build success |
| `published.sh` | Published | ocean | PyPI publish success |
| `deployed.sh` | Deployed | ocean | Deploy success |
| `tests-skipped.sh` | Tests Skipped | sunset | CI warning |
| `build-warning.sh` | Build Warning | sunset | CI warning |
| `tests-failed.sh` | Tests Failed | fire | CI test failure |
| `build-failed.sh` | Build Failed | fire | CI build failure |
| `deploy-failed.sh` | Deploy Failed | fire | CI deploy failure |

Font: `slant` (default, configurable via `BANNER_FONT`).

---

## Makefile Target

Added to `Makefile` alongside existing `test`, `test-quick`, `clean` targets:

```makefile
BANNER_FONT := slant

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

Usage:
```bash
make banners                      # slant font (default)
make banners BANNER_FONT=ogre     # regenerate with a different font
```

---

## CI Integration

### `ci.yml` — after `Run tests` step in each matrix job:

```yaml
- name: Show banner
  if: success()
  run: bash assets/bin/tests-passed.sh

- name: Show banner
  if: failure()
  run: bash assets/bin/tests-failed.sh
```

### `publish.yml` — after `Publish to PyPI` step:

```yaml
- name: Show banner
  if: success()
  run: bash assets/bin/published.sh

- name: Show banner
  if: failure()
  run: bash assets/bin/build-failed.sh
```

---

## Files Modified

| Action | Path |
|--------|------|
| Create (×9) | `assets/bin/*.sh` |
| Modify | `Makefile` |
| Modify | `.github/workflows/ci.yml` |
| Modify | `.github/workflows/publish.yml` |
