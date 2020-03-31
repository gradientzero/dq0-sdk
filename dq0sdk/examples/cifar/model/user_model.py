# -*- coding: utf-8 -*-
"""Neural Network model for CIFAR10 dataset.

Use this example to train a classifier on the CIFAR10 image data.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.tf.cifar10_network import CIFAR10Model


class UserModel(CIFAR10Model):
    """Convolutional Neural Network model implementation for Cifar10.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
