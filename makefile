# .PHONY tells Make these are not real files/folders to check for,
# but rather just names of our commands
.PHONY: help setup-local-dev test-local test-tox test-coverage dist-bundle-build publish-test publish clean

help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup-local-dev: ## Set up the development environment
	pip install -e .
	pip install -r requirements.txt

test-local: dev ## Run pytest for single environment testing
	pytest

test-tox: ## Run tests across multiple Python environments using tox
	tox

test-coverage: ## Run tests with coverage report (local development only)
	pytest --cov=clean_py --cov-report=term-missing

dist-bundle-build: clean ## Build both source distribution and wheel distribution
	python setup.py sdist bdist_wheel

publish-test: dist ## Build and publish package to TestPyPI
	@echo "Publishing to TestPyPI..."
	python -m twine upload --repository testpypi dist/*

publish: dist ## Build and publish package to PyPI
	@echo "Publishing to PyPI..."
	python -m twine upload dist/*

clean: ## Remove all build artifacts and temporary files
	@echo "Cleaning up build artifacts and cache files..."
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ venv/ .tox/ .coverage htmlcov/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -exec rm -f {} +
	@find . -type f -name ".coverage.*" -exec rm -f {} +

