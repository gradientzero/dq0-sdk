# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.model import Model

logger = logging.getLogger()


class UserModel(Model):
    """Derived from dq0sdk.models.Model class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        self.train_data, self.data = source.read()

        # preprocess data
        self.X_test, self.y_test, num_instances = source.preprocess()

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        pass

    def fit(self, **kwargs):
        """

        Train model on a dataset passed as input.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def save(self):
        """Saves the model.

        """
        pass

    def load(self):
        """Loads the model.

        """
        pass
