# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.models.tf import NeuralNetwork


class NeuralNetworkClassification(NeuralNetwork):
    """Neural Network multi class classification model
    """

    def __init__(self):
        super().__init__()

        # to instantiate the suitable model checker from dq0-core.dq0.util
        self.model_type = 'NeuralNetworkClassification'

        # calibrate posterior probabilities of the fitted model
        self.calibrate_posterior_probabilities = True

    def to_string(self):
        print('\nModel type is: ', self.model_type)
