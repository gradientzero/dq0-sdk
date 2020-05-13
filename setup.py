# -*- coding: utf-8 -*-
"""Setup script for DQ0 SDK.

Copyright 2020, Gradient Zero
All rights reserved
"""

from setuptools import find_packages, setup


# Version
VERSION = '0.1'

# Requirements
with open("requirements.txt") as f:
    install_requires = [line for line in f.read().splitlines()
                        if line and not line.startswith("#")]

# Setup
setup(
    name="dq0sdk",
    version=VERSION,
    description="DQ0 SDK",
    author="Gradient Zero",
    author_email="dq0@gradient0.com",
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=[
        "setuptools>=41.0.0",
        "pytest-runner~=5.2",
        "flake8~=3.7.9",
        "flake8-import-order~=0.18.1"
    ]
)
