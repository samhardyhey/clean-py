import glob
import logging
from pathlib import Path

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

    try:
        if path.is_dir():
            # recursively apply to all .py source within dir
            logging.info(f"Recursively cleaning directory: {path}")
            if py:
                for e in glob.iglob(f"{path.as_posix()}/**/*.py", recursive=True):
                    try:
                        logging.info(f"Cleaning file: {e}")
                        clean_py(e, autoflake, isort, black)
                    except Exception as e:
                        logging.error(f"Unable to clean file: {e}")
                        if verbose:
                            logging.exception("Detailed error:")
            if ipynb:
                # recursively apply to all .ipynb source within dir
                for e in glob.iglob(f"{path.as_posix()}/**/*.ipynb", recursive=True):
                    try:
                        logging.info(f"Cleaning file: {e}")
                        clean_ipynb(e, autoflake=autoflake, isort=isort, black=black)
                    except Exception as e:
                        logging.error(f"Unable to clean file: {e}")
                        if verbose:
                            logging.exception("Detailed error:")

        elif path.is_file():
            if py and path.suffix == ".py":
                try:
                    logging.info(f"Cleaning file: {path}")
                    clean_py(path, autoflake, isort, black)
                except Exception as e:
                    logging.error(f"Unable to clean file: {e}")
                    if verbose:
                        logging.exception("Detailed error:")

            elif ipynb and path.suffix == ".ipynb":
                try:
                    logging.info(f"Cleaning file: {path}")
                    clean_ipynb(path, autoflake=autoflake, isort=isort, black=black)
                except Exception as e:
                    logging.error(f"Unable to clean file: {e}")
                    if verbose:
                        logging.exception("Detailed error:")

            else:
                console.print(
                    f"[red]Error: Unable to clean {path} with current options[/red]"
                )
                raise typer.Exit(1)

        console.print("[green]Cleaning completed successfully![/green]")

    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        if verbose:
            logging.exception("Detailed error:")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
