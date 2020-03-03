# dq0-sdk

DQ0 Software Development Kit

This library is to be used by data scientists to create ML models the DQ0 way.

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

pip install -e git+https://github.com/gradientzero/dq0-sdk.git

Production / binary installation TBD

## Create wheel package
```bash
python setup.py sdist bdist_wheel
```
it will create at least two files in "dist".

## Usage
for a detailed description of how to setup, train and test and new mode see [dq0sdk/examples/yaml/readme.md](dq0sdk/examples/yaml/readme.md)