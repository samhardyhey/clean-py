from clean_py.clean_py import clean_python_code, clean_py, clean_ipynb
import pytest
from json import dump, load


def test_clean_source_apply_all(black_playground_template_input, apply_all):
    res = clean_python_code(black_playground_template_input)
    assert res == apply_all


def test_clean_source_apply_black(black_playground_template_input, black_only):
    res = clean_python_code(black_playground_template_input, isort=False, black=True, autoflake=False)
    assert res == black_only


# def test_clean_source_apply_isort(black_playground_template_input, isort_only):
#     res = clean_python_code(black_playground_template_input, isort=True, black=False, autoflake=False)
#     assert res == isort_only


def test_clean_source_apply_autoflake(black_playground_template_input, autoflake_only):
    res = clean_python_code(black_playground_template_input, isort=False, black=False, autoflake=True)
    assert res == autoflake_only


def test_clean_py(mocker, black_playground_template_input, black_only, autoflake_only):
    mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data=black_playground_template_input)
    )
    mock_create_file = mocker.patch('clean_py.clean_py.create_file')

    clean_py(
        py_file_path=pytest.example_script.as_posix(),
        isort=False,
        black=True,
        autoflake=False
    )

    mock_create_file.assert_called_once_with(
        pytest.example_script,
        black_only
    )

    mock_create_file.reset_mock()

    clean_py(
        py_file_path=pytest.example_script.as_posix(),
        isort=False,
        black=False,
        autoflake=True
    )

    mock_create_file.assert_called_once_with(
        pytest.example_script,
        autoflake_only
    )



"""
def clean_ipynb(ipynb_file_path, clear_output=True, autoflake=True, isort=True, black=True):
    # load, clean and write .ipynb source in-place, back to original file
    if clear_output:
        clear_ipynb_output(ipynb_file_path)

    with open(ipynb_file_path) as ipynb_file:
        ipynb_dict = load(ipynb_file)

    _clean_ipynb_cell = partial(
        clean_ipynb_cell,
        autoflake=autoflake,
        isort=isort,
        black=black
    )

    # mulithread the map operation
    processed_cells = pool.map(_clean_ipynb_cell, ipynb_dict["cells"])
    ipynb_dict["cells"] = processed_cells

    with open(ipynb_file_path, "w") as ipynb_file:
        dump(ipynb_dict, ipynb_file, indent=1)
        ipynb_file.write("\n")
"""


def test_clean_ipynb(mocker, ipynb_content, ipynb_autoflake_only, ipynb_isort_only, ipynb_black_only):
    # with open(pytest.example_notebook.as_posix()) as ipynb_file:
    #     ipynb_content = ipynb_file.read()
    mock_open = mocker.mock_open(read_data=ipynb_content)
    mocker.patch('builtins.open', mock_open)

    mock_dump = mocker.patch('clean_py.clean_py.dump')

    clean_ipynb(
        ipynb_file_path=pytest.example_notebook.as_posix(),
        clear_output=False,
        autoflake=True,
        isort=False,
        black=False
    )
    mock_dump.assert_called_once_with(
        ipynb_autoflake_only,
        mock_open.return_value,
        indent=1
    )
    mock_dump.reset_mock()

    clean_ipynb(
        ipynb_file_path=pytest.example_notebook.as_posix(),
        clear_output=False,
        autoflake=False,
        isort=True,
        black=False
    )
    mock_dump.assert_called_once_with(
        ipynb_isort_only,
        mock_open.return_value,
        indent=1
    )
    mock_dump.reset_mock()

    clean_ipynb(
        ipynb_file_path=pytest.example_notebook.as_posix(),
        clear_output=False,
        autoflake=False,
        isort=False,
        black=True
    )
    mock_dump.assert_called_once_with(
        ipynb_black_only,
        mock_open.return_value,
        indent=1
    )
    mock_dump.reset_mock()
