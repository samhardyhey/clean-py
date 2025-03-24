import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from clean_py.cli import app

# Get the test files directory
TEST_FILES_DIR = Path(__file__).parent / "test_files"
TEST_PY_FILE = TEST_FILES_DIR / "test.py"
TEST_IPYNB_FILE = TEST_FILES_DIR / "test.ipynb"

def setup_test_files():
    """Create test files if they don't exist"""
    TEST_FILES_DIR.mkdir(exist_ok=True)

    if not TEST_PY_FILE.exists():
        TEST_PY_FILE.write_text("def test():\n    pass\n")

    if not TEST_IPYNB_FILE.exists():
        TEST_IPYNB_FILE.write_text("""{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["print('hello')"]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 2
}""")

@pytest.fixture(autouse=True)
def setup():
    """Automatically set up test files before each test"""
    setup_test_files()

def test_cli_single_py_file():
    """Test CLI with a single Python file"""
    runner = CliRunner()
    result = runner.invoke(app, [str(TEST_PY_FILE)])
    assert result.exit_code == 0

def test_cli_single_ipynb_file():
    """Test CLI with a single Jupyter notebook"""
    runner = CliRunner()
    result = runner.invoke(app, [str(TEST_IPYNB_FILE)])
    assert result.exit_code == 0

def test_cli_directory():
    """Test CLI with a directory"""
    runner = CliRunner()
    result = runner.invoke(app, [str(TEST_FILES_DIR)])
    assert result.exit_code == 0

def test_cli_invalid_path():
    """Test CLI with an invalid path"""
    runner = CliRunner()
    result = runner.invoke(app, ["nonexistent_path"])
    assert result.exit_code == 1
    assert "Error: Path 'nonexistent_path' does not exist" in result.stdout