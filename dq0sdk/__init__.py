# -*- coding: utf-8 -*-
"""DQ0 SDK Main Package

This is the main dq0sdk package containing everything SDK related
"""

from . import data
from . import models

__all__ = [
    'version',
    'data',
    'models'
]

# dq0 sdk version
import pkg_resources  # part of setuptools
version = pkg_resources.require("dq0sdk")[0].version
del pkg_resources