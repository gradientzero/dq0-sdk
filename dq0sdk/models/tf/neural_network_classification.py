# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork


class NeuralNetworkClassification(NeuralNetwork):
    """Neural Network model implementation.

    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'NeuralNetworkClassification'
