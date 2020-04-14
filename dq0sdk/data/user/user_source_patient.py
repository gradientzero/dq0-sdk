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

from dq0sdk.data.patient.patient_source import PatientSource

logger = logging.getLogger()


class UserSource(PatientSource):
	"""User Data Source.

	Args:
		filepath (str): Absolute path to the data file.
	"""
	def __init__(self, filepath):
		super().__init__(filepath)

	

