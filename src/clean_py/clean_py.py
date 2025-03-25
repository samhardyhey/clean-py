import contextlib
from json import dump, load
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
from pathlib import Path
from subprocess import run
import logging
from typing import List, Dict, Any, Union

from autoflake import fix_code
from black import DEFAULT_LINE_LENGTH, FileMode, NothingChanged, format_file_contents
from isort import code

pool = Pool(cpu_count())


def remove_duplicate_cells(cells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate cells from a Jupyter notebook.

    Args:
        cells: List of notebook cell dictionaries.

    Returns:
        List of unique cells with duplicates removed.
    """
    cell_set_strings = []
    cell_set = []
    for e in cells:
        if e["source"] in cell_set_strings:
            continue
        cell_set_strings.append(e["source"])
        cell_set.append(e)
    return cell_set


def remove_empty_cells(cells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove empty cells from a Jupyter notebook.

    Args:
        cells: List of notebook cell dictionaries.

    Returns:
        List of cells with empty cells removed.
    """
    return [e for e in cells if len(e["source"]) > 2]


def remove_magics(source: str) -> str:
    """Remove Jupyter magic commands from cell source code.

    Args:
        source: Cell source code as string.

    Returns:
        Source code with magic commands removed.
    """
    # check for '%' in first token of each line
    non_magic_source = []
    # magics, as well as source queries
    invalid_source = ["%", "?"]
    for e in source.split("\n"):
        if len(e) == 0:
            continue
        if e[0] in invalid_source:
            continue
        else:
            non_magic_source.append(e)
    return "\n".join(non_magic_source)


def clean_python_code(
    python_source: str,
    isort: bool = True,
    black: bool = True,
    autoflake: bool = True,
    is_notebook_cell: bool = False,
) -> str:
    """Clean Python source code using various formatting tools.

    Args:
        python_source: Python source code to clean.
        isort: Whether to sort imports using isort.
        black: Whether to format code using black.
        autoflake: Whether to remove unused imports using autoflake.
        is_notebook_cell: Whether the source is from a notebook cell.

    Returns:
        Cleaned Python source code.
    """
    # run source code string through autoflake, isort, and black
    formatted_source = python_source

    # For notebook cells, only apply black formatting to preserve imports
    if is_notebook_cell:
        if black:
            mode = FileMode(
                line_length=DEFAULT_LINE_LENGTH,
                is_pyi=False,
                string_normalization=True,
            )
            with contextlib.suppress(NothingChanged):
                formatted_source = format_file_contents(
                    formatted_source, fast=True, mode=mode
                )
        return formatted_source

    # For regular Python files, apply all formatters
    if autoflake:
        formatted_source = fix_code(
            formatted_source,
            expand_star_imports=True,
            remove_all_unused_imports=True,
            remove_duplicate_keys=True,
            remove_unused_variables=True,
        )

    if isort:
        formatted_source = code(formatted_source)

    if black:
        mode = FileMode(
            line_length=DEFAULT_LINE_LENGTH,
            is_pyi=False,
            string_normalization=True,
        )
        with contextlib.suppress(NothingChanged):
            formatted_source = format_file_contents(
                formatted_source, fast=True, mode=mode
            )

    return formatted_source


def create_file(file_path: Path, contents: str) -> None:
    """Create or overwrite a file with given contents.

    Args:
        file_path: Path to the file.
        contents: Contents to write to the file.
    """
    file_path.touch()
    with file_path.open("w", encoding="utf-8") as f:
        f.write(contents)


def clean_py(py_file_path: Union[str, Path], autoflake: bool = True, isort: bool = True, black: bool = True) -> None:
    """Clean a Python file using various formatting tools.

    Args:
        py_file_path: Path to the Python file.
        autoflake: Whether to remove unused imports using autoflake.
        isort: Whether to sort imports using isort.
        black: Whether to format code using black.
    """
    py_file_path = Path(py_file_path)
    with open(py_file_path, "r") as file:
        source = file.read()

    clean_lines = clean_python_code(source, autoflake=autoflake, isort=isort, black=black)
    create_file(py_file_path, clean_lines)


def clear_ipynb_output(ipynb_file_path: Union[str, Path]) -> None:
    """Clear cell outputs and reset execution counts in a Jupyter notebook.

    Args:
        ipynb_file_path: Path to the notebook file.
    """
    run(
        (
            "jupyter",
            "nbconvert",
            "--ClearOutputPreprocessor.enabled=True",
            "--inplace",
            str(ipynb_file_path),
        ),
        check=True,
    )


def clean_ipynb_cell(cell_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Clean a single Jupyter notebook cell.

    Args:
        cell_dict: Dictionary containing cell data.

    Returns:
        Cleaned cell dictionary.
    """
    if cell_dict["cell_type"] != "code":
        return cell_dict
    try:
        # Handle both string and list source inputs
        source = cell_dict["source"]
        if isinstance(source, list):
            source = "".join(source)

        # Preserve imports by setting is_notebook_cell=True
        clean_source = clean_python_code(source, is_notebook_cell=True)

        # Split into lines and ensure each line (except last) ends with newline
        clean_lines = clean_source.split("\n")
        if clean_lines[-1] == "":
            clean_lines = clean_lines[:-1]
        if clean_lines:
            clean_lines = [line + "\n" for line in clean_lines[:-1]] + [clean_lines[-1]]

        cell_dict["source"] = clean_lines
        return cell_dict

    except Exception as e:
        # return original cell dict otherwise
        logging.error(f"Error cleaning cell: {e}")
        return cell_dict


def clean_ipynb(
    ipynb_file_path: Union[str, Path],
    clear_output: bool = True,
    autoflake: bool = True,
    isort: bool = True,
    black: bool = True,
) -> None:
    """Clean a Jupyter notebook file.

    Args:
        ipynb_file_path: Path to the notebook file.
        clear_output: Whether to clear cell outputs.
        autoflake: Whether to remove unused imports using autoflake.
        isort: Whether to sort imports using isort.
        black: Whether to format code using black.
    """
    ipynb_file_path = Path(ipynb_file_path)
    if clear_output:
        clear_ipynb_output(ipynb_file_path)

    with open(ipynb_file_path) as ipynb_file:
        ipynb_dict = load(ipynb_file)

    # multithread the map operation
    processed_cells = pool.map(clean_ipynb_cell, ipynb_dict["cells"])
    ipynb_dict["cells"] = processed_cells

    with open(ipynb_file_path, "w") as ipynb_file:
        dump(ipynb_dict, ipynb_file, indent=1)
        ipynb_file.write("\n")
