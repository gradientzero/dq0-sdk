# -*- coding: utf-8 -*-
"""User Image Source for CIFAR-10 dataset.

This is a template for user defined Image sources (i.e., data sources for
image datasets).

This template class derives from ImageSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.image.image_source import ImageSource

import tensorflow as tf

logger = logging.getLogger()


class UserSource(ImageSource):
    """
    Image Source for CIFAR-10 image dataset.

    """
    def __init__(self):
        super().__init__()

    def _load_data(self):
        """Loads the image data.

        Child classes need to implement this function!

        Returns:
            X_train_np_a (:obj:`numpy.ndarray`): X train data
            X_test_np_a (:obj:`numpy.ndarray`): X test data
            y_train_np_a (:obj:`numpy.ndarray`): y train data
            y_test_np_a (:obj:`numpy.ndarray`): y test data
        """

        (X_train_np_a, y_train_np_a), (X_test_np_a, y_test_np_a) = \
            tf.keras.datasets.cifar10.load_data()

        logger.debug('Loaded CIFAR-10 image dataset')

        return X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a
