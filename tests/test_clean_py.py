from pathlib import Path
import pytest
from clean_py.clean_py import (
    clean_python_code,
    remove_duplicate_cells,
    remove_empty_cells,
    remove_magics,
    create_file,
    clean_ipynb_cell,
)


def test_clean_source_apply_all(black_playground_template_input, apply_all):
    res = clean_python_code(black_playground_template_input)
    assert res == apply_all


def test_clean_source_apply_black(black_playground_template_input, black_only):
    res = clean_python_code(
        black_playground_template_input, isort=False, black=True, autoflake=False
    )
    assert res == black_only


# def test_clean_source_apply_isort(black_playground_template_input, isort_only):
#     res = clean_python_code(black_playground_template_input, isort=True, black=False, autoflake=False)
#     assert res == isort_only


def test_clean_source_apply_autoflake(black_playground_template_input, autoflake_only):
    res = clean_python_code(
        black_playground_template_input, isort=False, black=False, autoflake=True
    )
    assert res == autoflake_only


def test_remove_duplicate_cells():
    cells = [
        {"source": "print(1)", "cell_type": "code"},
        {"source": "print(2)", "cell_type": "code"},
        {"source": "print(1)", "cell_type": "code"},  # Duplicate
    ]
    result = remove_duplicate_cells(cells)
    assert len(result) == 2
    assert result[0]["source"] == "print(1)"
    assert result[1]["source"] == "print(2)"


def test_remove_empty_cells():
    cells = [
        {"source": "print(1)", "cell_type": "code"},
        {"source": "", "cell_type": "code"},  # Empty
        {"source": "  ", "cell_type": "code"},  # Whitespace only
        {"source": "print(2)", "cell_type": "code"},
    ]
    result = remove_empty_cells(cells)
    assert len(result) == 2
    assert result[0]["source"] == "print(1)"
    assert result[1]["source"] == "print(2)"


def test_remove_magics():
    source = """print(1)
%matplotlib inline
?help
print(2)"""
    result = remove_magics(source)
    assert result == "print(1)\nprint(2)"


def test_create_file(tmp_path):
    test_file = tmp_path / "test.txt"
    content = "test content"
    create_file(test_file, content)
    assert test_file.exists()
    assert test_file.read_text() == content


def test_clean_ipynb_cell_code():
    cell = {
        "cell_type": "code",
        "source": ["import os\n", "\n", "print ( 1)"],  # Source should be a list in notebooks
        "execution_count": 1,
        "outputs": [],
    }
    result = clean_ipynb_cell(cell)
    # The function should clean the code and return a list of lines
    assert isinstance(result["source"], list)
    # The code should be formatted
    formatted_code = "".join(result["source"])
    assert "import os" in formatted_code
    assert "print(1)" in formatted_code


def test_clean_ipynb_cell_markdown():
    cell = {
        "cell_type": "markdown",
        "source": "# Test",
        "metadata": {},
    }
    result = clean_ipynb_cell(cell)
    assert result == cell  # Markdown cells should be unchanged


def test_clean_ipynb_cell_error():
    cell = {
        "cell_type": "code",
        "source": "invalid python code :",  # This will cause a syntax error
        "execution_count": 1,
        "outputs": [],
    }
    result = clean_ipynb_cell(cell)
    assert result == cell  # Should return original cell on error
