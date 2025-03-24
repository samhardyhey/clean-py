from pathlib import Path
import re

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Core dependencies - these are used by tox and when installing the package
CORE_REQUIREMENTS = [
    "black==25.1.0",
    "isort==6.0.1",
    "jupyter==1.1.1",
    "autoflake==2.3.1",
    "jupyter_contrib_nbextensions==0.7.0",
    "pytest==8.3.5",
]

# For development, try to read from requirements.txt if it exists
try:
    REQUIREMENTS = [
        line.strip()
        for line in (this_directory / "requirements.txt").read_text().splitlines()
        if line.strip()
        and not line.startswith("#")
        and not re.match(r"^(tox|build|twine)", line.strip())
    ]
except FileNotFoundError:
    REQUIREMENTS = CORE_REQUIREMENTS

setup(
    name="clean_py",
    use_scm_version={
        "local_scheme": "no-local-version",
        "version_scheme": "post-release",
    },
    setup_requires=['setuptools_scm'],
    url="https://github.com/samhardyhey/clean-py",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["clean_py=clean_py.cli:main"]},
    python_requires=">=3.6",
    install_requires=CORE_REQUIREMENTS,  # Use direct dependencies for tox
    long_description=long_description,
    long_description_content_type="text/markdown",
)
