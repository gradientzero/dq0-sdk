# -*- coding: utf-8 -*-
"""Neural network pytests.

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf import NeuralNetwork


def test_set_params():
    neural_network = NeuralNetwork()
    neural_network.learning_rate = 0.3
    assert neural_network.learning_rate == 0.3
