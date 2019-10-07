### Clean Py
A small CLI program capable of cleaning ```.ipynb``` and ```.py``` source. Tidy and remove redundant imports (via [autoflake](https://github.com/myint/autoflake)), sort imports (via [isort](https://github.com/timothycrosley/isort)), lint and format source code in a standardised way (via [black](https://github.com/ambv/black)). Apply equally to ```.py``` or ```.ipynb``` files. Additionally, clear all ```.ipynb``` cell outputs and execution counts. Forked from KwatMe's orginal [repo](https://github.com/KwatME/clean_ipynb).

### 1.0 Up and Running
Via git pip:
```sh
pip install clean-py
```

Via source:
```sh
git clone https://github.com/samhardyhey/clean_py
cd clean_py
pip install .
```

### 2.0 Usage
Clean ```.ipynb``` source:
```sh
clean_py a_single_notebook.ipynb
```

Or ```.py``` source:
```sh
clean_py a_single_script.py
```

Or an entire directory recursively:
```sh
clean_py <some_dir_containing_py_ipynb_source>
```

Clean with specific features if necessary:
```sh
clean_py <some_dir_containing_py_ipynb_source> -py True -isort True -black False -autoflake False
```

A full list of parameters can be found via:
```sh
clean_py --help
```
### 3.0 Tests
Via:
```sh
python -m pytest clean_py/tests/
```

### 4.0 Packaging
Create dist `.whl` and `.tar` archives via:
```py
python setup.py sdist bdist_wheel
```
Push to main pypi repo via:
```py
twine upload dist/*
```