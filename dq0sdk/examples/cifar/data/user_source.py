# -*- coding: utf-8 -*-
"""CIFAR10 User Data Source.

This is an example for the CIFAR10 data set.

Installation notes:
    It loads the data set via `tf.keras.datasets.cifar10.load_data()` therefore
    requiring an active internet connection. Once the data is downloaded it is
    cached in the user's home directory.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.cifar10 import CIFAR10Source


class UserSource(CIFAR10Source):
    """User Data Source.

    Implementation for CIFAR10 dataset.
    """
    def __init__(self):
        super().__init__()
