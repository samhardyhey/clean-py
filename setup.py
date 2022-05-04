from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIREMENTS = [
    "black==22.3.0",
    "isort==4.3.21",
    "jupyter==1.0.0",
    "autoflake==1.4",
    "jupyter_contrib_nbextensions==0.5.1",
    "pytest==7.0.1",
]

setup(
    name="clean_py",
    version="0.4",
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
