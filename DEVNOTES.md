
## Dev Setup

Create a suitable virtual environment:

```bash
conda create -n dq0-sdk python=3.6
source activate dq0-sdk
```

And install dependencies

```bash
pip install -r requirements.txt
```

## Generate sphinx documentation

Generate modules .rst files first automatically:
```bash
sphinx-apidoc -M -o ./docs/source/generated ./dq0sdk -f -e
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



## Dev Guide

This repository contains production-grade software. Thus, strict enterprise software development guidelines are to be respected.
The git workflow looks like this:

![git workflow](git.png)

Feature branches are merged to the development branch via pull requests and prior code review.
Continuous integration is implemented via github actions for both development and master branch.

### Code style and documentation

Python code styles follows the PEP 8 style guide and is inforced by flake8. CI builds will fail if flake8 produces errors.

Code documentation follows the python google docstring format: [https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

Code documentation is generated with the included sphinx library and makefile in the doc subdirectory.


## Installation

Install in setup tools development mode:

```bash
pip install -e git+https://github.com/gradientzero/dq0-sdk.git
````

Production / binary installation TBD

## Create wheel package
```bash
python setup.py sdist bdist_wheel
```
it will create at least two files in "dist".

## Usage
for a detailed description of how to setup, train and test and new mode see [dq0sdk/examples/yaml/readme.md](dq0sdk/examples/yaml/readme.md)