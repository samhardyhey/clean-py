import glob
import logging
from pathlib import Path
import json

import typer
from rich.console import Console
from rich.logging import RichHandler

from .clean_py import clean_ipynb, clean_py

# Configure rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

console = Console()
app = typer.Typer(
    name="clean-py",
    help="Auto-lint .py and .ipynb files with autoflake, isort and black",
    add_completion=False,
)


@app.command()
def main(
    path: str = typer.Argument(..., help="File or directory to clean"),
    py: bool = typer.Option(True, help="Apply to .py source"),
    ipynb: bool = typer.Option(True, help="Apply to .ipynb source"),
    autoflake: bool = typer.Option(True, help="Apply autoflake to source"),
    isort: bool = typer.Option(True, help="Apply isort to source"),
    black: bool = typer.Option(True, help="Apply black to source"),
    verbose: bool = typer.Option(False, help="Enable verbose output"),
):
    """
    Clean Python files and Jupyter notebooks using various code formatting tools.

    The tool can process both individual files and entire directories recursively.
    For Python files, it can apply autoflake, isort, and black formatting.
    For Jupyter notebooks, it can also clear outputs and reset execution counts.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    path = Path(path)
    if not path.exists():
        console.print(f"[red]Error: Path '{path}' does not exist[/red]")
        raise typer.Exit(1)

    has_errors = False
    try:
        if path.is_file():
            if py and path.suffix == ".py":
                try:
                    logging.info(f"Cleaning file: {path}")
                    clean_py(path, autoflake, isort, black)
                except Exception as e:
                    console.print(f"[yellow]Warning: Unable to clean file {path}: {e}[/yellow]")
                    if verbose:
                        logging.exception("Detailed error:")
                    has_errors = True

            elif ipynb and path.suffix == ".ipynb":
                try:
                    logging.info(f"Cleaning file: {path}")
                    # Try to load the notebook first to validate JSON
                    with open(path) as f:
                        try:
                            json.load(f)  # Use json.load instead of load to be explicit
                        except json.JSONDecodeError:
                            console.print(f"[red]Error: Invalid notebook format in {path}[/red]")
                            raise typer.Exit(code=1)
                    clean_ipynb(path, autoflake=autoflake, isort=isort, black=black)
                except json.JSONDecodeError:
                    console.print(f"[red]Error: Invalid notebook format in {path}[/red]")
                    raise typer.Exit(code=1)
                except Exception as e:
                    console.print(f"[yellow]Warning: Unable to clean file {path}: {e}[/yellow]")
                    if verbose:
                        logging.exception("Detailed error:")
                    has_errors = True

            else:
                console.print(
                    f"[yellow]Warning: Skipping {path} (unsupported file type)[/yellow]"
                )

        else:  # path is a directory
            for file_path in path.rglob("*"):
                if py and file_path.suffix == ".py":
                    try:
                        logging.info(f"Cleaning file: {file_path}")
                        clean_py(file_path, autoflake, isort, black)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Unable to clean file {file_path}: {e}[/yellow]")
                        if verbose:
                            logging.exception("Detailed error:")
                        has_errors = True

                elif ipynb and file_path.suffix == ".ipynb":
                    try:
                        logging.info(f"Cleaning file: {file_path}")
                        # Try to load the notebook first to validate JSON
                        with open(file_path) as f:
                            try:
                                json.load(f)  # Use json.load instead of load to be explicit
                            except json.JSONDecodeError:
                                console.print(f"[yellow]Warning: Invalid notebook format in {file_path}[/yellow]")
                                has_errors = True
                                continue
                        clean_ipynb(file_path, autoflake=autoflake, isort=isort, black=black)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Unable to clean file {file_path}: {e}[/yellow]")
                        if verbose:
                            logging.exception("Detailed error:")
                        has_errors = True

        if has_errors:
            console.print("[yellow]Cleaning completed with some warnings.[/yellow]")
        else:
            console.print("[green]Cleaning completed successfully![/green]")

    except Exception as e:
        console.print(f"[red]Error: An unexpected error occurred: {e}[/red]")
        if verbose:
            logging.exception("Detailed error:")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
