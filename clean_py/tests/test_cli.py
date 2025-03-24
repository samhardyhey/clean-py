import subprocess
from pathlib import Path

import pytest

# Get the test files directory
pytest.file_dir = Path(__file__).parent / "test_files"
pytest.py_file = pytest.file_dir / "test.py"
pytest.ipynb_file = pytest.file_dir / "test.ipynb"

def test_cli_single_py_file():
    """Test CLI with a single Python file"""
    res = subprocess.run(["python", "-m", "clean_py.cli", str(pytest.py_file)])
    assert res.returncode == 0

def test_cli_single_ipynb_file():
    """Test CLI with a single Jupyter notebook"""
    res = subprocess.run(["python", "-m", "clean_py.cli", str(pytest.ipynb_file)])
    assert res.returncode == 0

def test_cli_file_dir():
    """Test CLI with a directory"""
    res = subprocess.run(["python", "-m", "clean_py.cli", str(pytest.file_dir)])
    assert res.returncode == 0

def test_cli_invalid_path():
    """Test CLI with an invalid path"""
    res = subprocess.run(["python", "-m", "clean_py.cli", "nonexistent_path"])
    assert res.returncode == 1

def test_cli_help():
    """Test CLI help command"""
    res = subprocess.run(["python", "-m", "clean_py.cli", "--help"], capture_output=True)
    assert res.returncode == 0
    assert b"Auto-lint .py and .ipynb files" in res.stdout
