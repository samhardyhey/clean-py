from pathlib import Path
import re

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read core dependencies from requirements.txt
REQUIREMENTS = [
    line.strip()
    for line in (this_directory / "requirements.txt").read_text().splitlines()
    if line.strip()
    and not line.startswith("#")
    and not re.match(r"^(tox|build|twine)", line.strip())
]

setup(
    name="clean_py",
    version="0.5",
    url="https://github.com/samhardyhey/clean-py",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["clean_py=clean_py.cli:main"]},
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
