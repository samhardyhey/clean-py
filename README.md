## Clean Py
A small CLI program designed to automatically lint ```.ipynb``` and ```.py``` source code. Tidy and remove redundant imports (via [autoflake](https://github.com/myint/autoflake)), sort imports (via [isort](https://github.com/timothycrosley/isort)), lint and format source code in a standardised way (via [black](https://github.com/ambv/black)). Additionally, clear all ```.ipynb``` cell outputs and execution counts. Forked from KwatMe's orginal [repo](https://github.com/KwatME/clean_ipynb).

## 1.0 Up and Running
Via pip:
```sh
pip install clean-py
```

Or clone directly:
```sh
git clone https://github.com/samhardyhey/clean_py
cd clean_py
pip install .
```

## 2.0 Usage
Clean a single file:
```sh
clean_py a_single_notebook.ipynb
clean_py a_single_script.py
```

Or recurse an input dir:
```sh
clean_py <source/dir>
```

Clean with specific features if necessary:
```sh
clean_py <source/dir> -py True -isort True -black False -autoflake False
```

## 3.0 Tests
Via:
```sh
pytest ./pytest
```

## 4.0 Packaging
- Update version within `setup.py`
- Create dist `.whl` and `.tar` archives via:
```py
python setup.py sdist bdist_wheel
```
Push to main pypi repo via:
```py
twine upload dist/*
```