PYTHON_VERSIONS := 3.11 3.12 3.13

.PHONY: test test-quick clean

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

## clean: remove build artifacts and caches
clean:
	rm -rf dist/ .pytest_cache/ __pycache__/ src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## help: show this help
help:
	@grep -E '^## ' Makefile | sed 's/^## /  /'
