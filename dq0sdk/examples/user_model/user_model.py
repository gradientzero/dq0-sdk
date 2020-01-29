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

from dq0sdk.models.model import Model

class UserModel(Model):
    """Derived from dq0sdk.models.Model class

    Model classes provide a setup method as well as the fit and predict
    ML model functions.
    """
    def __init__(self):
        super().__init__()

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

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

    def predict(self, x, **kwargs):
        """Model predict function.

        Implementing child classes will perform model scoring here.

        The implemented child class version will be final (non-derivable).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        pass

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

    def save(self, name, version):
        """Saves the model.

        Implementing child classes should use this function to save the
        model in binary format on local storage.

        The implemented child class version will be final (non-derivable).

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        pass

    def load(self, name, version):
        """Loads the model.

        Implementing child classes should use this function to load the
        model from local storage.

        The implemented child class version will be final (non-derivable).

        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """
        pass
