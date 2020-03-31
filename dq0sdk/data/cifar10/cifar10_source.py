# -*- coding: utf-8 -*-
"""CIFAR10 User Data Source.

This is a data source implementation for the CIFAR10 data set.

Installation notes:
    It loads the data set via `tf.keras.datasets.cifar10.load_data()` therefore
    requiring an active internet connection. Once the data is downloaded it is
    cached in the user's home directory.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.source import Source
from dq0sdk.data.utils import util

from matplotlib import pyplot as plt

import numpy as np

import tensorflow as tf


logger = logging.getLogger()


class CIFAR10Source(Source):
    """CIFAR Data Source.

    Implementation for CIFAR10 dataset.
    """
    def __init__(self):
        super().__init__()
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                            'dog', 'frog', 'horse', 'ship', 'truck']

    def read(self, num_instances_to_load=None, num_images_to_plot=None):
        """Load the CIFAR10 data with `tf.keras.datasets.cifar10.load_data()`.

        Args:
            num_instances_to_load (int, optional): Set to limit the number of images to read.
            num_images_to_plot (int, optional): Set to plot n number of images.

        Returns:
            X data array, y data array
        """
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                            'dog', 'frog', 'horse', 'ship', 'truck']

        logger.debug('Loading CIFAR10 dataset')

        (X_train_np_a, y_train_np_a), (X_test_np_a, y_test_np_a) = \
            tf.keras.datasets.cifar10.load_data()

        # merge train and test
        X_np_a, y_np_a = util.concatenate_train_test_datasets(
            X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a)

        # scale pixel values to be between 0 and 1
        max_pixel_intensity = 255
        X_np_a = preprocessing.scale_pixels(X_np_a, max_pixel_intensity)

        if num_instances_to_load is not None:
            X_np_a = X_np_a[:num_instances_to_load]
            y_np_a = y_np_a[:num_instances_to_load]

        logger.debug('Dataset size: X=%s, y=%s' % (X_np_a.shape, y_np_a.shape))

        if num_images_to_plot is not None:
            self._plot_first_few_images(X_np_a, y_np_a, num_images_to_plot)

        return X_np_a, y_np_a

    def _plot_first_few_images(self, X_np_a, y_np_a, num_images_to_plot):
        """Plots the first n images."""
        plt.figure(figsize=(10, 10))
        for i in range(num_images_to_plot):
            plt.subplot(np.ceil(num_images_to_plot / 5), 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(X_np_a[i], cmap=plt.cm.binary)
            # The CIFAR labels happen to be arrays,
            # which is why you need the extra index
            plt.xlabel(self.class_names[y_np_a[i][0]])
        plt.show()

    def preprocess(self):
        """Preprocess CIFAR data."""
        pass

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        shape = ''
        if self.read_allowed:
            try:
                X, y = self.read()
                shape = '{}'.format(X.shape)
            except Exception as e:
                logger.debug('Could not get meta info of content. {}'.format(e))

        permissions = []
        if self.read_allowed:
            permissions.append('read')
        if self.meta_allowed:
            permissions.append('meta')
        if self.types_allowed:
            permissions.append('types')
        if self.stats_allowed:
            permissions.append('stats')
        if self.sample_allowed:
            permissions.append('sample')

        return {
            "name": self.name,
            "type": 'cifar',
            "shape": shape,
            "permissions": permissions
        }
