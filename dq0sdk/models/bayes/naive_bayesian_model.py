# -*- coding: utf-8 -*-
"""Naive Bayesian Model class

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os
import pickle

from dq0sdk.models.model import Model


logger = logging.getLogger()


class NaiveBayesianModel(Model):
    """Naive Bayesian classifier implementation.

    Simple model representing a Bayesian classifier.
    """

    def __init__(self, model_path):
        super().__init__(model_path)

        self.model_type = 'NaiveBayesianClassifier'  # to instantiate the
        # suitable model checker from dq0-core.dq0.util

    def to_string(self):
        print('\nModel type is: ', self.model_type)

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (str): The name of the model
            version (int): The version of the model
        """

        file_path = '{}/{}/{}.pickle'.format(self.model_path, version, name)
        # create target directory and all intermediate directories if not
        # existing
        file_path_dirs = os.path.dirname(file_path)
        if not os.path.exists(file_path_dirs):
            os.makedirs(file_path_dirs)

        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (str): The name of the model
            version (int): The version of the model
        """

        file_path = '{}/{}/{}.pickle'.format(self.model_path, version, name)

        with open(file_path, 'rb') as file:
            self.model = pickle.load(file)
