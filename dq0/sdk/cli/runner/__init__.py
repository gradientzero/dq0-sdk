# -*- coding: utf-8 -*-
"""Runner manages a running experiment.

There is an abstract base class for runner and two implementing child classes:
    * ModelRunner
    * DataRunner
"""

from .data_runner import DataRunner
from .model_runner import ModelRunner

__all__ = [
    'DataRunner',
    'ModelRunner'
]
