# -*- coding: utf-8 -*-
"""User Data Source.

This is a template for user defined data sources.
When training a model on a certain deta source dq0-core is looking for a
UserSource class that is to be used as the custom data source implementation.

This template class derives from Source. Actual implementations should derive
from child classes like CSVSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.cifar10.cifar10_source import CIFAR10Source

logger = logging.getLogger()


class UserSource(CIFAR10Source):
	"""User Data Source.

	Args:
		filepath (str): Absolute path to the data file.
	"""
	def __init__(self,file_path):
		super().__init__(file_path=file_path)
