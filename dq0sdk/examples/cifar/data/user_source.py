# -*- coding: utf-8 -*-
"""CIFAR10 User Data Source.

This is a data source implementation for the CIFAR10 data set.

More information on CIFAR10: https://www.cs.toronto.edu/~kriz/cifar.html

Installation notes:
    It loads the data set via `tf.keras.datasets.cifar10.load_data()` therefore
    requiring an active internet connection. Once the data is downloaded it is
    cached in the user's home directory.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.data.image import ImageSource

import tensorflow as tf


class UserSource(ImageSource):
    """Data Source for CIFAR10 dataset.

    From the CIFAR description: The CIFAR-10 dataset consists of 60000 32x32
    colour images in 10 classes, with 6000 images per class. There are 50000
    training images and 10000 test images.

    Attributes:
        class_names (:obj:`list`): List of CIFAR class names to use

    """
    def __init__(self):
        super().__init__()

    def _load_data(self):
        """Loads the CIFAR10 data.

        Returns:
            X_train_np_a (:obj:`numpy.ndarray`): X train data
            X_test_np_a (:obj:`numpy.ndarray`): X test data
            y_train_np_a (:obj:`numpy.ndarray`): y train data
            y_test_np_a (:obj:`numpy.ndarray`): y test data
        """
        (X_train_np_a, y_train_np_a), (X_test_np_a, y_test_np_a) = \
            tf.keras.datasets.cifar10.load_data()
        return X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a
