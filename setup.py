from setuptools import find_packages, setup

setup(
    name="clean_py",
    version="0.1",
    url="https://github.com/samhardyhey/clean-py",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["clean_py=clean_py.cli:main_wrapper"]},
    python_requires=">=3.6",
    install_requires=("black", "wasabi", "isort", "jupyter", "autoflake", "plac", "jupyter_contrib_nbextensions", "pytest", "isort==4.3.21"),
)
