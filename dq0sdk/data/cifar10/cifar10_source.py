# -*- coding: utf-8 -*-
"""
Adult dataset loading

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Paolo Campigotto <pc@gradient0.com>

Copyright 2019, Gradient Zero
"""

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.source import Source

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import tensorflow as tf


class CIFAR10Source(Source):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                            'dog', 'frog', 'horse', 'ship', 'truck']

    def read(self, num_instances_to_load=None, num_images_to_plot=None):
        """

        :param num_instances_to_load:
        :param num_images_to_plot:
        :return:
        """

        print('\nLoad CIFAR10 dataset')

        (X_train_np_a, y_train_np_a), (X_test_np_a, y_test_np_a) = \
            tf.keras.datasets.cifar10.load_data()

        X_np_a, y_np_a = self._concatenate_tr_te_datasets(
            X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a)

        if num_instances_to_load is not None:
            X_np_a = X_np_a[:num_instances_to_load]
            y_np_a = y_np_a[:num_instances_to_load]

        print('Dataset size: X=%s, y=%s' % (X_np_a.shape, y_np_a.shape))

        if num_images_to_plot is not None:
            self._plot_first_few_images(X_np_a, y_np_a, num_images_to_plot)

        return X_np_a, y_np_a

    def _concatenate_tr_te_datasets(self, X_train_np_a, X_test_np_a,
                                    y_train_np_a, y_test_np_a):
        """
        :param X_train_np_a: numpy array
        :param X_test_np_a: numpy array
        :param y_train_np_a: numpy (also non-dimensional) array
        :param y_test_np_a: numpy (also non-dimensional) array

        :return: X, y
        """
        X_np_a = np.append(X_train_np_a, X_test_np_a, axis=0)
        if y_train_np_a.ndim < 2:
            # transform one-dimensional array into column vector via newaxis
            y_train_np_a = y_train_np_a[:, np.newaxis]
            y_test_np_a = y_test_np_a[:, np.newaxis]

        y_np_a = np.append(y_train_np_a, y_test_np_a, axis=0)

        return X_np_a, y_np_a

    def _plot_first_few_images(self, X_np_a, y_np_a, num_images_to_plot):

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

    def get_preprocessed_X_y(self, num_instances_to_load=None,
                             num_images_to_plot=None):
        """
        DEPRECATED. Will be removed in future releases.
        :param num_instances_to_load:
        :param num_images_to_plot:
        :return:
        """

        X_np_a, y_np_a, = self.read(num_instances_to_load, num_images_to_plot)
        X_np_a = self.preprocess(X=X_np_a)

        return X_np_a, y_np_a

    def preprocess(self, force=False, **kwargs):

        assert isinstance(kwargs['X'], np.ndarray)

        X_np_a = kwargs['X']

        # scale pixel values to be between 0 and 1
        max_pixel_intensity = 255
        X_np_a = preprocessing.scale_pixels(X_np_a, max_pixel_intensity)

        return X_np_a

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
