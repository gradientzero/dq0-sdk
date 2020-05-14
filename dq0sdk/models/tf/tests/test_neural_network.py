# -*- coding: utf-8 -*-
"""Neural network pytests.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf.neural_network_classification import NeuralNetworkClassification


def test_set_params():
    neural_network = NeuralNetworkClassification('')
    neural_network.learning_rate = 0.3
    assert neural_network.learning_rate == 0.3
