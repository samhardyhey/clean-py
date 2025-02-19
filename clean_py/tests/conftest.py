import os
from pathlib import Path

import pytest


def pytest_configure():
    pytest.test_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    pytest.file_dir = pytest.test_dir / "test_files"
    pytest.example_notebook = pytest.file_dir / "example_notebook.ipynb"
    pytest.example_script = pytest.file_dir / "example_script.py"


@pytest.fixture
def black_playground_template_input():
    return """from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc
import sklearn
from glob import glob

x = {  'a':37,'b':42,

'c':927}

x = 123456789.123456789E123456789

if very_long_variable_name is not None and \
 very_long_variable_name.field > 0 or \
 very_long_variable_name.is_debug:
 z = 'hello '+'world'
else:
 world = 'world'
 a = 'hello {}'.format(world)
 f = rf'hello {world}'
if (this
and that): y = 'hello ''world'#FIXME: https://github.com/python/black/issues/26
class Foo  (     object  ):
  def f    (self   ):
    return       37*-2
  def g(self, x,y=42):
      return y
def f  (   a: List[ int ]) :
  return      37-a[42-u :  y**3]
def very_important_function(template: str,*variables,file: os.PathLike,debug:bool=False,):
    with open(file, "w") as f:
     ...
# fmt: off
custom_formatting = [
    0,  1,  2,
    3,  4,  5,
    6,  7,  8,
]
# fmt: on
regular_formatting = [
    0,  1,  2,
    3,  4,  5,
    6,  7,  8,
]"""


@pytest.fixture
def apply_all():
    return """x = {"a": 37, "b": 42, "c": 927}\n\nx = 123456789.123456789e123456789\n\nif (\n    very_long_variable_name is not None\n    and very_long_variable_name.field > 0\n    or very_long_variable_name.is_debug\n):\n    z = "hello " + "world"\nelse:\n    world = "world"\n    a = "hello {}".format(world)\n    f = rf"hello {world}"\nif this and that:\n    y = "hello " "world"  # FIXME: https://github.com/python/black/issues/26\n\n\nclass Foo(object):\n    def f(self):\n        return 37 * -2\n\n    def g(self, x, y=42):\n        return y\n\n\ndef f(a: List[int]):\n    return 37 - a[42 - u : y**3]\n\n\ndef very_important_function(\n    template: str,\n    *variables,\n    file: os.PathLike,\n    debug: bool = False,\n):\n    with open(file, "w") as f:\n        ...\n\n\n# fmt: off\ncustom_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]\n# fmt: on\nregular_formatting = [\n    0,\n    1,\n    2,\n    3,\n    4,\n    5,\n    6,\n    7,\n    8,\n]\n"""


@pytest.fixture
def isort_only():
    return """from glob import glob\n\nimport sklearn\n\nfrom seven_dwwarfs import Bashful, Doc, Dopey, Grumpy, Happy, Sleepy, Sneezy\n\nx = {  \'a\':37,\'b\':42,\n\n\'c\':927}\n\nx = 123456789.123456789E123456789\n\nif very_long_variable_name is not None and  very_long_variable_name.field > 0 or  very_long_variable_name.is_debug:\n z = \'hello \'+\'world\'\nelse:\n world = \'world\'\n a = \'hello {}\'.format(world)\n f = rf\'hello {world}\'\nif (this\nand that): y = \'hello \'\'world\'#FIXME: https://github.com/python/black/issues/26\nclass Foo  (     object  ):\n  def f    (self   ):\n    return       37*-2\n  def g(self, x,y=42):\n      return y\ndef f  (   a: List[ int ]) :\n  return      37-a[42-u :  y**3]\ndef very_important_function(template: str,*variables,file: os.PathLike,debug:bool=False,):\n    with open(file, "w") as f:\n     ...\n# fmt: off\ncustom_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]\n# fmt: on\nregular_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]\n"""


@pytest.fixture
def black_only():
    return """from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc\nimport sklearn\nfrom glob import glob\n\nx = {"a": 37, "b": 42, "c": 927}\n\nx = 123456789.123456789e123456789\n\nif (\n    very_long_variable_name is not None\n    and very_long_variable_name.field > 0\n    or very_long_variable_name.is_debug\n):\n    z = "hello " + "world"\nelse:\n    world = "world"\n    a = "hello {}".format(world)\n    f = rf"hello {world}"\nif this and that:\n    y = "hello " "world"  # FIXME: https://github.com/python/black/issues/26\n\n\nclass Foo(object):\n    def f(self):\n        return 37 * -2\n\n    def g(self, x, y=42):\n        return y\n\n\ndef f(a: List[int]):\n    return 37 - a[42 - u : y**3]\n\n\ndef very_important_function(\n    template: str,\n    *variables,\n    file: os.PathLike,\n    debug: bool = False,\n):\n    with open(file, "w") as f:\n        ...\n\n\n# fmt: off\ncustom_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]\n# fmt: on\nregular_formatting = [\n    0,\n    1,\n    2,\n    3,\n    4,\n    5,\n    6,\n    7,\n    8,\n]\n"""


@pytest.fixture
def autoflake_only():
    return """\nx = {  \'a\':37,\'b\':42,\n\n\'c\':927}\n\nx = 123456789.123456789E123456789\n\nif very_long_variable_name is not None and  very_long_variable_name.field > 0 or  very_long_variable_name.is_debug:\n z = \'hello \'+\'world\'\nelse:\n world = \'world\'\n a = \'hello {}\'.format(world)\n f = rf\'hello {world}\'\nif (this\nand that): y = \'hello \'\'world\'#FIXME: https://github.com/python/black/issues/26\nclass Foo  (     object  ):\n  def f    (self   ):\n    return       37*-2\n  def g(self, x,y=42):\n      return y\ndef f  (   a: List[ int ]) :\n  return      37-a[42-u :  y**3]\ndef very_important_function(template: str,*variables,file: os.PathLike,debug:bool=False,):\n    with open(file, "w") as f:\n     ...\n# fmt: off\ncustom_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]\n# fmt: on\nregular_formatting = [\n    0,  1,  2,\n    3,  4,  5,\n    6,  7,  8,\n]"""
