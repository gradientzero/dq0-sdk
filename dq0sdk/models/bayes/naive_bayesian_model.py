# -*- coding: utf-8 -*-
"""Naive Bayesian Model class

Copyright 2020, Gradient Zero
All rights reserved
"""

import copy
import logging
import os
import pickle

from dq0sdk.models.model import Model

import sklearn


logger = logging.getLogger()


class NaiveBayesianModel(Model):
    """Naive Bayesian classifier implementation.

    Simple model representing a Bayesian classifier.
    """

    def __init__(self, model_path):
        super().__init__(model_path)

        # to instantiate the suitable model checker from dq0-core.dq0.util
        self.model_type = 'NaiveBayesianClassifier'

        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

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

    def get_clone(self, trained=False):
        """
        Generates a new model with the same parameters, if they are not fit on
        the training data.

        Generates a deep copy of the model without actually
        copying any attached dataset. It yields a new model with the same
        parameters that has not been fit on any data. Parameters fit to
        the training data like, e.g., model weights, are re-initialized in the
        clone.

        Args:
            trained: if `True`, maintains current state including trained model
                weights, etc. Otherwise, returns an unfitted model with the same
                initialization params.

        Returns:
            deep copy of model

        """

        if trained:
            new_scikit_model = copy.deepcopy(self.model)
        else:
            # Clone does a deep copy of the model without actually copying
            # attached data. It yields a new model with the same parameters
            # that has not been fit on any data.
            new_scikit_model = sklearn.base.clone(self.model)
            # keep class labels if they have been specified
            try:
                new_scikit_model.classes_ = self.model.classes_
            except AttributeError:
                pass

        # performance boosting: do not (deep) copy any data that will be
        # discarded immediately after deep copying
        tmp_storage = {'model': self.model, 'X_train': self.X_train,
                       'y_train': self.y_train, 'X_test': self.X_test,
                       'y_test': self.y_test, 'model_path': self.model_path}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.model_path = None
        self.data_source = None

        # model clone
        # new_model = self.__class__(model_path=None)
        new_model = copy.deepcopy(self)
        new_model.model = new_scikit_model

        # recover attributes temporarily removed for efficient deep copying
        for key, value in tmp_storage.items():
            self.__setattr__(key, value)

        return new_model
