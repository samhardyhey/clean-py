# Clean-Py 🧹

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
### Development Workflow
1. Create a new branch from `dev` for your feature/fix
2. Make your changes and ensure tests pass
3. Submit a pull request to `dev`
4. After review and approval, merge to `dev`
5. When ready for release, create a pull request from `dev` to `main`

### Project Structure
- `src/clean_py/` - Main package code
- `tests/` - Test files

### Common Development Commands
See the Makefile for common, useful dev commands.

## Credits
This project is a fork of [clean_ipynb](https://github.com/KwatME/clean_ipynb) by Kwat Medetgul-Ernar, with significant modifications and improvements. We gratefully acknowledge the original work that made this project possible.