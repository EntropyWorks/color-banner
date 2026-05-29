PYTHON_VERSIONS := 3.11 3.12 3.13
BANNER_FONT     := slant

.PHONY: test test-quick clean banners

## test: run the full test suite against all supported Python versions (mirrors CI)
test:
	@failed=0; \
	for version in $(PYTHON_VERSIONS); do \
		echo ""; \
		echo "══════════════════════════════════════════"; \
		echo "  Python $$version"; \
		echo "══════════════════════════════════════════"; \
		uv run --python $$version pytest tests/ -v || failed=1; \
	done; \
	echo ""; \
	if [ $$failed -eq 0 ]; then \
		echo "✓ All Python versions passed"; \
	else \
		echo "✗ One or more Python versions failed"; \
		exit 1; \
	fi

## test-quick: run the test suite against the default Python version only
test-quick:
	uv run pytest tests/ -v

## banners: generate self-contained banner scripts into assets/bin/
banners:
	@mkdir -p assets/bin
	@uv run color-banner "Tests Passed"    --palette ocean  --font $(BANNER_FONT) --function-name show_tests_passed   --export assets/bin/tests-passed.sh
	@uv run color-banner "Build Complete"  --palette ocean  --font $(BANNER_FONT) --function-name show_build_complete  --export assets/bin/build-complete.sh
	@uv run color-banner "Published"       --palette ocean  --font $(BANNER_FONT) --function-name show_published       --export assets/bin/published.sh
	@uv run color-banner "Deployed"        --palette ocean  --font $(BANNER_FONT) --function-name show_deployed        --export assets/bin/deployed.sh
	@uv run color-banner "Tests Skipped"   --palette sunset --font $(BANNER_FONT) --function-name show_tests_skipped   --export assets/bin/tests-skipped.sh
	@uv run color-banner "Build Warning"   --palette sunset --font $(BANNER_FONT) --function-name show_build_warning   --export assets/bin/build-warning.sh
	@uv run color-banner "Tests Failed"    --palette fire   --font $(BANNER_FONT) --function-name show_tests_failed    --export assets/bin/tests-failed.sh
	@uv run color-banner "Build Failed"    --palette fire   --font $(BANNER_FONT) --function-name show_build_failed    --export assets/bin/build-failed.sh
	@uv run color-banner "Deploy Failed"   --palette fire   --font $(BANNER_FONT) --function-name show_deploy_failed   --export assets/bin/deploy-failed.sh
	@echo "Generated assets/bin/ with font: $(BANNER_FONT)"

## clean: remove build artifacts and caches
clean:
	rm -rf dist/ .pytest_cache/ __pycache__/ src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## help: show this help
help:
	@grep -E '^## ' Makefile | sed 's/^## /  /'
