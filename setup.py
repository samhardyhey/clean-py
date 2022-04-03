from setuptools import find_packages, setup

with open("./requirements.txt") as f:
    REQUIREMENTS = f.readlines()

setup(
    name="clean_py",
    version="0.2",
    url="https://github.com/samhardyhey/clean-py",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["clean_py=clean_py.cli:main"]},
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
)
