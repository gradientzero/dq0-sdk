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
        super().__init__(name='CIFAR10', **kwargs)
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

        if num_instances_to_load is not None:
            X_train_np_a = X_train_np_a[:num_instances_to_load]
            y_train_np_a = y_train_np_a[:num_instances_to_load]
            X_test_np_a = X_test_np_a[:num_instances_to_load]
            y_test_np_a = y_test_np_a[:num_instances_to_load]

        print('Train-dataset size: X=%s, y=%s' % (X_train_np_a.shape,
                                                  y_train_np_a.shape))
        print('Test-dataset size: X=%s, y=%s' % (X_test_np_a.shape,
                                                 y_test_np_a.shape))

        if num_images_to_plot is not None:
            self._plot_first_few_images(X_train_np_a, y_train_np_a,
                                        num_images_to_plot)

        return X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a

    def _plot_first_few_images(self, X_train_np_a, y_train_np_a,
                               num_images_to_plot):

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

    def get_preprocessed_X_y_train_and_X_y_test(self,
                                                num_instances_to_load=None,
                                                num_images_to_plot=None
                                                ):

        X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a = \
            self.read(num_instances_to_load, num_images_to_plot)

        X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a = self.preprocess(
            X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a
        )

        target_feature = None  # for compatibility with Pandas DataFrame case

        return X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a, \
            target_feature

    def preprocess(self, X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a,
                   force=False):

        # Make 1-dimensional arrays
        # y_train_np_a = np.ravel(y_train_np_a)
        # y_test_np_a = np.ravel(y_test_np_a)

        # Scale pixel values to be between 0 and 1
        max_pixel_intensity = 255
        X_train_np_a = preprocessing.scale_pixels(X_train_np_a,
                                                  max_pixel_intensity)
        X_test_np_a = preprocessing.scale_pixels(X_test_np_a,
                                                 max_pixel_intensity)

        return X_train_np_a, X_test_np_a, y_train_np_a, y_test_np_a

    def save_preprocessed_tr_and_te_datasets(self, X_train, X_test,
                                             y_train, y_test,
                                             working_folder):
        """

        :param X_train: Pandas Dataframe or numpy array
        :param X_test:  Pandas Dataframe or numpy array
        :param y_train: Pandas Series or numpy (also non-dimensional) array
        :param y_test: Pandas Series or numpy (also non-dimensional) array
        :param working_folder: str with file path
        :return:
        """

        if isinstance(X_train, pd.DataFrame):

            pd.concat([X_train, y_train], axis=1).to_csv(
                working_folder + 'preprocessed_training_data.csv', index=False)
            pd.concat([X_test, y_test], axis=1).to_csv(
                working_folder + 'preprocessed_test_data.csv', index=False)

        elif isinstance(X_train, np.ndarray):

            if y_train.ndim < 2:
                # transform one-dimensional array into column vector via
                # newaxis
                y_train = y_train[:, np.newaxis]
                y_test = y_test[:, np.newaxis]

            if X_train.ndim <= 2:
                np.savetxt(working_folder + 'preprocessed_training_X.csv',
                           X_train, delimiter=',')
                np.savetxt(working_folder + 'preprocessed_test_X.csv',
                           X_test, delimiter=',')
            else:
                np.save(working_folder + 'preprocessed_training_X.npy',
                        X_train)
                np.save(working_folder + 'preprocessed_test_X.npy', X_test)

            np.savetxt(working_folder + 'preprocessed_training_y.csv',
                       y_train, delimiter=',')
            np.savetxt(working_folder + 'preprocessed_test_y.csv',
                       y_test, delimiter=',')

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
