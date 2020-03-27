# -*- coding: utf-8 -*-
"""Neural network pytests.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork


def test_set_params():
    neural_network = NeuralNetwork('')
    neural_network.learning_rate = 0.3
    assert neural_network.learning_rate == 0.3
