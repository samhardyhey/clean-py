# .PHONY tells Make these are not real files/folders to check for,
# but rather just names of our commands
.PHONY: help test dist upload multi-test clean dev

help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

test-local: dev ## Run pytest for single environment testing
	pytest

test-tox: ## Run tests across multiple Python environments using tox
	tox

dist: clean ## Build both source distribution and wheel distribution
	python setup.py sdist bdist_wheel

upload: dist ## Upload the built distributions to PyPI
	twine upload dist/*

clean: ## Remove all build artifacts and temporary files
	@echo "Cleaning up build artifacts and cache files..."
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ venv/ .tox/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -exec rm -f {} +

setup-local-dev: ## Set up the development environment
	pip install -e .
	pip install -r requirements.txt