## Dev Setup

Create a suitable virtual environment:

```bash
conda create -n dq0 python=3.7
source activate dq0
```

Install postgresql dependency for psycopg2:
```bash
brew install postgresql
```

And now install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Helper to resolve dependency conflicts:
```bash
# pip install pipdeptree
pipdeptree
```

## Run tests

Use pytest for testings dq0-sdk completely:
```bash
# important not to use 'pytest .' only
# explicitly use your current python environment
python -m pytest
```

To test "slow" marked tests only, use:
```bash
python -m pytest -m slow
```

To test all non "slow" marked tests only, use:
```bash
python -m pytest -m "not slow"
```

Or one specific method:
```bash
# ignore setup.cfg with parameter "c"
python -m pytest -c /dev/null tests/test_dummies.py::test_slow
```

## Format code

Use autopep8 to auto format code:
```bash
python -m autopep8 --in-place --aggressive --aggressive -r dq0
```


## Generate sphinx documentation

Generate modules .rst files first automatically:
```bash
sphinx-apidoc -M -o ./docs/source ./dq0 -f -e --implicit-namespaces
```
This will (re-)generate multiple .rst file for each module / submodule and class.

Execute makefile inside folder doc:
```bash
(cd docs && make html)
```

generate pdf:
```bash
(cd docs && sphinx-build -b rinoh source build/rinoh)
```


## Installation

Install in setup tools development mode:

```bash
pip install -e git+https://github.com/gradientzero/dq0-sdk.git

# or from source
pip install .
````

Production / binary installation TBD

## Create wheel package
```bash
python setup.py sdist bdist_wheel
```
it will create at least two files in "dist".
