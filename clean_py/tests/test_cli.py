import subprocess

import pytest


def test_cli_single_py_file():
    res = subprocess.run(["clean_py", pytest.example_script])
    assert res.returncode == 0


def test_cli_single_ipynb_file():
    res = subprocess.run(["clean_py", pytest.example_notebook])
    assert res.returncode == 0


def test_cli_file_dir():
    res = subprocess.run(["clean_py", pytest.file_dir])
    assert res.returncode == 0
