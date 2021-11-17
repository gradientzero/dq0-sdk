# -*- coding: utf-8 -*-
"""Preprocess abstract base class

The source class serves as the base class for all preprocessing in user models.

Implementing subclasses have to define at least run

Copyright 2020, Gradient Zero
All rights reserved
"""
from abc import abstractmethod


class BasePreprocess(object):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self, x, y=None, train=False):
        """ Execute User defined preprocessing

        used by UserModel and predict to preprocess data

        Args:
            - x: raw input data
            - y: raw input data labels
            - train [bool]: store transformer parameters

        Return:
            - x [pd.DataFrame, np.ndarray]: model input
            - y [pd.Series, np.array]: labels
        """
        pass

    def predict(self, x):
        """ wrapper of run for mlflow """
        return self.run(x=x)
