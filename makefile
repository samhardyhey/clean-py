# .PHONY tells Make these are not real files/folders to check for,
# but rather just names of our commands
.PHONY: help setup-local-dev test-local test-tox test-coverage dist-bundle-build publish-test publish clean tag-release version-history cleanup-testpypi cleanup-pypi

help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup-local-dev: ## Set up the development environment
	@if [ ! -d "venv" ]; then \
		echo "Creating Python virtual environment..."; \
		python -m venv venv; \
	fi
	@echo "Installing package in development mode..."
	@./venv/bin/pip install -e .
	@echo "\nSetup complete! To activate the virtual environment, run:\n\n    source venv/bin/activate\n"

test-local: ## Run pytest for single environment testing
	pytest tests

test-tox: ## Run tests across multiple Python environments using tox
	tox

test-coverage: ## Run tests with coverage report (local development only)
	pytest tests --cov=src/clean_py --cov-report=term-missing

dist-bundle-build: clean ## Build both source distribution and wheel distribution
	python -m build

publish-test: dist-bundle-build ## Build and publish package to TestPyPI
	@echo "Publishing to TestPyPI..."
	python -m twine upload --repository testpypi dist/* || test $$? -eq 400

publish: dist-bundle-build ## Build and publish package to PyPI
	@echo "Publishing to PyPI..."
	python -m twine upload --verbose dist/*

clean: ## Remove all build artifacts and temporary files
	@echo "Cleaning up build artifacts and cache files..."
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ venv/ .tox/ .coverage htmlcov/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -exec rm -f {} +
	@find . -type f -name ".coverage.*" -exec rm -f {} +

tag-release: ## Create and push a new release tag (usage: make tag-release VERSION=1.2.3)
	@if [ "$(VERSION)" = "" ]; then \
		echo "Error: VERSION is required. Usage: make tag-release VERSION=1.2.3"; \
		exit 1; \
	fi
	@echo "Creating tag v$(VERSION)..."
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)

version-history: ## Show version history and help with semantic versioning
	@echo "Current versions on PyPI:"
	@curl -s https://pypi.org/pypi/clean-py/json | grep -o '"version":"[^"]*"' | cut -d'"' -f4 | sort -V
	@echo "\nGit tags:"
	@git tag -l | sort -V
	@echo "\nSemantic Versioning Guide:"
	@echo "  MAJOR.MINOR.PATCH[-PRERELEASE]"
	@echo "  - MAJOR: Breaking changes (e.g., 1.0.0 -> 2.0.0)"
	@echo "  - MINOR: New features, no breaking changes (e.g., 1.0.0 -> 1.1.0)"
	@echo "  - PATCH: Bug fixes only (e.g., 1.0.0 -> 1.0.1)"
	@echo "  - PRERELEASE: Development versions (e.g., 1.0.0-alpha.1)"

cleanup-testpypi: ## Clean up old versions from TestPyPI (requires PYPI_CLEANUP_PASSWORD env var)
	@echo "Cleaning up TestPyPI versions..."
	@read -p "Enter PyPI username: " username; \
	pypi-cleanup -p clean-py \
		-r '.*\.(dev|post|a|b|rc)\d+.*' \
		--do-it \
		-y \
		-t https://test.pypi.org/ \
		-u $$username \
		-v

cleanup-pypi: ## Clean up old versions from PyPI (requires PYPI_CLEANUP_PASSWORD env var)
	@echo "Cleaning up PyPI versions..."
	@read -p "Enter PyPI username: " username; \
	pypi-cleanup -p clean-py \
		-r '.*\.(dev|post|a|b|rc)\d+.*' \
		--do-it \
		-y \
		-u $$username \
		-v

