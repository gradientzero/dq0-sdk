#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.patient_network import PatientModel

logger = logging.getLogger()


class UserModel(PatientModel):

	def __init__(self, model_path):
		super().__init__(model_path)
