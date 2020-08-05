# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.models.tf import NeuralNetwork

# import tensorflow.compat.v1 as tf


class NeuralNetworkRegression(NeuralNetwork):
    """Neural Network model implementation.

    """

    def __init__(self):
        super().__init__()

        # to instantiate the suitable model checker from dq0-core.dq0.util
        self.model_type = 'NeuralNetworkRegression'

        self.metrics = ['mean_squared_error']

    def to_string(self):
        print('\nModel type is: ', self.model_type)
