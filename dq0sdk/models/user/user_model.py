#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>
"""

import logging

from dq0sdk.models.tf import NeuralNetwork

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    """Derived from dq0sdk.models.Model class

    Model classes provide a setup method as well as the fit and predict
    ML model functions.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        self.data = source.read()

    def setup_model(self, **kwargs):
        """Setup model function

        Implementing child classes can use this method to define the
        model.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def prepare(self, **kwargs):
        """called before model fit on every run.

        Implementing child classes can use this method to prepare
        data for model training (preprocess data).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def fit(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
        """
        pass

    def fit_dp(self, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
        """
        pass

    def predict(self, x, **kwargs):
        """Model predict function.

        Implementing child classes will perform model scoring here.

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def evaluate(self, x, y, verbose=0, **kwargs):
        """Model predict and evluate.

        TODO: define returned metrics

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            metrics: to be defined!
        """
        pass
