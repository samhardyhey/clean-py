# Clean-Py 🧹

CLI tool for automated Python code cleanup and standardization. Formats both `.py` and `.ipynb` files using industry-standard tools.

## Features
- 🔄 Import optimization (autoflake)
- 📝 Import sorting (isort)
- ✨ Code formatting (black)
- 📓 Notebook cleanup
  - Clear cell outputs
  - Reset execution counts
  - Format code cells

## Installation
```bash
# Via pip
pip install clean-py

# Or from source
git clone https://github.com/samhardyhey/clean_py
cd clean_py
pip install .
```

## Usage
```bash
# Clean single file
clean_py notebook.ipynb
clean_py script.py

# Clean directory
clean_py path/to/dir

# Selective cleaning
clean_py path/to/dir -py True -isort True -black False -autoflake False
```

## Development
```bash
# Run tests
pytest

# Multi-environment testing
tox

# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

## Structure
- 🔧 `clean_py/` # Core package
  - `clean_py.py` # Main logic
  - `cli.py` # Command interface
  - `tests/` # Test suite

## Credits
Forked from [KwatMe's original repo](https://github.com/KwatME/clean_ipynb).

*Note: Remember to update version in `setup.py` before distribution.*