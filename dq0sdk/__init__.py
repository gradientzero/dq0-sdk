# -*- coding: utf-8 -*-
"""DQ0 SDK Main Package

This is the main dq0sdk package containing everything SDK related
"""

import pkg_resources  # part of setuptools

from . import data
from . import models

# dq0 sdk version
version = pkg_resources.require("dq0sdk")[0].version
del pkg_resources

__all__ = [
    'version',
    'data',
    'models'
]
