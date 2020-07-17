# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.models.tf import NeuralNetwork


class NeuralNetworkMultiClassClassification(NeuralNetwork):
    """Neural Network multi class classification model
    """

    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'NeuralNetworkMultiClassClassification'

    def to_string(self):
        print('\nModel type is: ', self.model_type)
