# -*- coding: utf-8 -*-
"""Setup script for DQ0 SDK.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from setuptools import find_namespace_packages, setup

from setuptools_cythonize import get_cmdclass


# meta information
VERSION = '1.0.0'
try:
    import dq0.sdk
    VERSION = dq0.sdk.version
except ImportError:
    pass

NAME = 'dq0-sdk'
DESCRIPTION = 'DQ0 SDK Runtime'

# Get the long description from the README file
LONG_DESCRIPTION = ''
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    LONG_DESCRIPTION = f.read()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

AUTHOR = 'Gradient Zero',
AUTHOR_EMAIL = 'dq0@gradient0.com',
URL = 'https://www.dq0.io'
SETUP_REQUIRES = [
    'setuptools>=41.0.0',
    'pytest-runner~=5.2',
    'flake8~=3.8.1',
    'flake8-import-order~=0.18.1',
]

PACKAGES = find_namespace_packages(include=['dq0.*'])  # find_packages()

# Requirements
INSTALL_REQUIRES = ['']
with open('requirements.txt') as f:
    INSTALL_REQUIRES = [line for line in f.read().splitlines()
                        if line and not line.startswith('#')]

# Extras requirements (big_query)
BIG_QUERY = ['']
with open('requirements-big_query.txt') as f:
    BIG_QUERY = [line for line in f.read().splitlines()
                        if line and not line.startswith('#')]

# Extras requirements (snowflake)
SNOWFLAKE = ['']
with open('requirements-snowflake.txt') as f:
    SNOWFLAKE = [line for line in f.read().splitlines()
                        if line and not line.startswith('#')]

EXTRA_REQUIRE = {
    "big_query" : BIG_QUERY,
    "snowflake" : SNOWFLAKE,
}


# Setup
setup(
    cmdclass=get_cmdclass(),
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    extras_require=EXTRA_REQUIRE,
    include_package_data=False,
)
