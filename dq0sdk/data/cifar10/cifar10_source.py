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

import logging

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.source import Source
from dq0sdk.data.utils import util

from matplotlib import pyplot as plt

import numpy as np

import tensorflow as tf

logger = logging.getLogger()


logger = logging.getLogger()


class CIFAR10Source(Source):
    """Data Source for CIFAR10 dataset.

    From the CIFAR description: The CIFAR-10 dataset consists of 60000 32x32
    colour images in 10 classes, with 6000 images per class. There are 50000
    training images and 10000 test images.

    Attributes:
        class_names (:obj:`list`): List of CIFAR class names to use

    """
    def __init__(self):
        super().__init__()
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                            'dog', 'frog', 'horse', 'ship', 'truck']

    def read(self, num_instances_to_load=None, num_images_to_plot=None):
        """Read CIFAR10 data.

        Read the CIFAR10 datset with tf.keras.datasets.cifar10.load_data()

        Note:
            To first load the dataset an internet connection is required. This
            is not allowed in DQ0. The initial loading should therefore be
            performed outside of the quarantine. Once loaded the locally cached
            version is used.

        Args:
            num_instances_to_load (int, optional): Optional number of maximum instances
            num_images_to_plot (int, optional): Optionally plot n images

        Returns:
            X_train_np_a (:obj:`numpy.ndarray`): X train data
            X_test_np_a (:obj:`numpy.ndarray`): X test data
            y_train_np_a (:obj:`numpy.ndarray`): y train data
            y_test_np_a (:obj:`numpy.ndarray`): y test data
        """
        logger.debug('Load CIFAR10 dataset')

        # load data
        (X_train_np_a, y_train_np_a), (X_test_np_a, y_test_np_a) = \
            tf.keras.datasets.cifar10.load_data()

        # merge data
        X_np_a, y_np_a = util.concatenate_train_test_datasets(
            X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a)

        # preprocess data
        max_pixel_intensity = 255
        X_np_a = preprocessing.scale_pixels(X_np_a, max_pixel_intensity)

        # limit data
        if num_instances_to_load is not None:
            X_np_a = X_np_a[:num_instances_to_load]
            y_np_a = y_np_a[:num_instances_to_load]

        logger.debug('Dataset size: X=%s, y=%s' % (X_np_a.shape, y_np_a.shape))

        # plot
        if num_images_to_plot is not None:
            self._plot_first_few_images(X_np_a, y_np_a, num_images_to_plot)

        return X_np_a, y_np_a

    def _plot_first_few_images(self, X_train_np_a, y_train_np_a,
                               num_images_to_plot):
        """Plot the num_images_to_plot first images."""
        plt.figure(figsize=(10, 10))
        for i in range(num_images_to_plot):
            plt.subplot(np.ceil(num_images_to_plot / 5), 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(X_train_np_a[i], cmap=plt.cm.binary)
            # The CIFAR labels happen to be arrays,
            # which is why you need the extra index
            plt.xlabel(self.class_names[y_train_np_a[i][0]])
        plt.show()

    def preprocess(self, X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a,
                   force=False):
        """Preprocess the loaded data."""
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
