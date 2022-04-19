import argparse
import glob
import logging
from pathlib import Path

from .clean_py import clean_ipynb, clean_py

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(
    prog="clean_py",
    description="Auto-lint .py and .ipynb files with autoflake, isort and black",
)
parser.add_argument("path", type=str, help="File or dir to clean")
parser.add_argument("--py", type=bool, default=True, required=False, help="Apply to .py source")
parser.add_argument("--ipynb", type=bool, default=True, help="Apply to .ipynb source")
parser.add_argument("--autoflake", type=bool, default=True, help="Apply autoflake to source")
parser.add_argument("--isort", type=bool, default=True, help="Apply isort to source")
parser.add_argument("--black", type=bool, default=True, help="Apply black to source")
args = parser.parse_args()


def main():
    path = Path(args.path)
    if not path.exists():
        raise ValueError("Provide a valid path to a file or directory")

    if path.is_dir():
        # recursively apply to all .py source within dir
        logging.info(f"Recursively cleaning directory: {path}")
        if args.py:
            for e in glob.iglob(f"{path.as_posix()}/**/*.py", recursive=True):
                try:
                    logging.info(f"Cleaning file: {e}")
                    clean_py(e, args.autoflake, args.isort, args.black)
                except Exception:
                    logging.error(f"Unable to clean file: {e}")
        if args.ipynb:
            # recursively apply to all .ipynb source within dir
            for e in glob.iglob(f"{path.as_posix()}/**/*.ipynb", recursive=True):
                try:
                    logging.info(f"Cleaning file: {e}")
                    clean_ipynb(e, args.autoflake, args.isort, args.black)
                except Exception:
                    logging.error(f"Unable to clean file: {e}")

    if path.is_file():
        if args.py and path.suffix == ".py":
            try:
                logging.info(f"Cleaning file: {path}")
                clean_py(path, args.autoflake, args.isort, args.black)
            except Exception:
                logging.error(f"Unable to clean file: {path}")

        elif args.ipynb and path.suffix == ".ipynb":
            try:
                logging.info(f"Cleaning file: {path}")
                clean_ipynb(path, args.autoflake, args.isort, args.black)
            except Exception:
                logging.error(f"Unable to clean file: {path}")

        else:
            raise ValueError(f"Unable to clean {path} with args! Double check your args..")
