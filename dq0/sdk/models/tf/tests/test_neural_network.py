# -*- coding: utf-8 -*-
"""Neural network pytests.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.models.tf.neural_network_classification import NeuralNetworkClassification


class ConcreteClass(NeuralNetworkClassification):
    def setup_data(self):
        pass

    def setup_model(self):
        pass


def test_set_params():
    neural_network = ConcreteClass('')
    neural_network.learning_rate = 0.3
    assert neural_network.learning_rate == 0.3
