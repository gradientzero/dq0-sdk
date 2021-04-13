# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.models.tf import NeuralNetwork


class NeuralNetworkMultiClassClassification(NeuralNetwork):
    """Neural Network multi class classification model."""

    def __init__(self):
        super().__init__()
        self.model_type = 'NeuralNetworkMultiClassClassification'

        # calibrate posterior probabilities of the fitted model
        self.calibrate_posterior_probabilities = False

    def to_string(self):
        print('\nModel type is: ', self.model_type)
