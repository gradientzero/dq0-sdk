# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.models.model import Model

logger = logging.getLogger()


class UserModel(Model):
    """Derived from dq0.sdk.models.Model class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        pass

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        pass

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        pass

    def fit(self, **kwargs):
        """

        Train model on a dataset passed as input.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def save(self, path):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            path (:obj:`str`): The model path
        """
        pass

    def load(self, path):
        """Loads the model.

        Load the model from local storage.

        Args:
            path (:obj:`str`): The model path
        """
        pass
