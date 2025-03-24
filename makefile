# .PHONY tells Make these are not real files/folders to check for,
# but rather just names of our commands
.PHONY: help test dist upload multi-test clean

# Default target that prints all commands
help:
	@echo "Available commands:"
	@echo "  test        - Run pytest for single environment testing"
	@echo "  multi-test  - Run tests across multiple Python environments using tox"
	@echo "  dist        - Build both source distribution and wheel distribution"
	@echo "  upload      - Upload the built distributions to PyPI"
	@echo "  clean       - Remove all build artifacts and temporary files"

# Run pytest for single environment testing
test:
	pytest

# Run tests across multiple Python environments using tox
multi-test:
	tox

# Build both source distribution and wheel distribution
# Depends on clean to ensure fresh builds
dist: clean
	python setup.py sdist bdist_wheel

# Upload the built distributions to PyPI
# Depends on dist to ensure we have the latest build
upload: dist
	twine upload dist/*

# Remove all build artifacts and temporary files
clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ venv/