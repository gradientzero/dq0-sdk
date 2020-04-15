# -*- coding: utf-8 -*-
"""Neural Network multi class classification model

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork


class NeuralNetworkMultiClassClassification(NeuralNetwork):
    """Neural Network multi class classification model
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'NeuralNetworkMultiClassClassification'
