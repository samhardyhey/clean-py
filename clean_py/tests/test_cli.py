import subprocess
from sys import modules

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


def test_call_main_single_py_file(mocker):
    autoflake = True
    isort = False
    black = True

    clean_py_main = load_main_function(
        mocker=mocker,
        path=pytest.example_script.as_posix(),
        autoflake=autoflake,
        isort=isort,
        black=black
    )

    mock_clean_py = mocker.patch('clean_py.cli.clean_py')

    clean_py_main()

    mock_clean_py.assert_called_once_with(
        py_file_path=pytest.example_script,
        autoflake=autoflake,
        isort=isort,
        black=black
    )


def test_call_cli_single_ipynb_file(mocker):
    autoflake = False
    isort = True
    black = False

    clean_py_main = load_main_function(
        mocker=mocker,
        path=pytest.example_notebook.as_posix(),
        autoflake=autoflake,
        isort=isort,
        black=black
    )

    mock_clean_ipynb = mocker.patch('clean_py.cli.clean_ipynb')

    clean_py_main()

    mock_clean_ipynb.assert_called_once_with(
        ipynb_file_path=pytest.example_notebook,
        clear_output=True,
        autoflake=autoflake,
        isort=isort,
        black=black
    )


def test_call_cli_file_dir(mocker):
    autoflake = False
    isort = False
    black = False

    clean_py_main = load_main_function(
        mocker=mocker,
        path=pytest.file_dir.as_posix(),
        autoflake=autoflake,
        isort=isort,
        black=black
    )

    mock_clean_py = mocker.patch('clean_py.cli.clean_py')
    mock_clean_ipynb = mocker.patch('clean_py.cli.clean_ipynb')

    clean_py_main()

    mock_clean_py.assert_called_once_with(
        py_file_path=pytest.example_script.as_posix(),
        autoflake=autoflake,
        isort=isort,
        black=black
    )

    mock_clean_ipynb.assert_called_once_with(
        ipynb_file_path=pytest.example_notebook.as_posix(),
        clear_output=True,
        autoflake=autoflake,
        isort=isort,
        black=black
    )


def load_main_function(mocker, path: str, autoflake: bool = True, isort: bool = True, black: bool = True):
    mocker.patch(
        'argparse._sys.argv',
        [
            'clean_py', path,
            '--autoflake', str(autoflake),
            '--isort', str(isort),
            '--black', str(black)
        ]
    )

    for m in ['clean_py.cli', 'clean_py.cli']:
        if m in modules:
            del modules[m]

    from clean_py.cli import main as clean_py_main

    return clean_py_main
