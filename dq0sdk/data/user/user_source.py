# -*- coding: utf-8 -*-
"""User Data Source.

This is a template for user defined data sources.
When training a model on a certain deta source dq0-core is looking for a
UserSource class that is to be used as the custom data source implementation.

This template class derives from Source. Actual implementations should derive
from child classes like CSVSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.source import Source
from dq0sdk.data.preprocessing import preprocessing

from matplotlib import pyplot as plt

import numpy as np

import pandas as pd

import tensorflow as tf


logger = logging.getLogger()


class UserSource(Source):
    """User Data Source.

    Template. Real implementations should derive from Source child classes.
    For example: UserSource(CSVSource)

    Args:
        filepath (str): Absolute path to the data file.
    """
    # def __init__(self, filepath):
        # super().__init__()
        # self.filepath = filepath

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
