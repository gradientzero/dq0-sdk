# -*- coding: utf-8 -*-
"""Data Source for adult test dataset.

The test set is contained in the subfolder "data"

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.source import Source
from dq0sdk.data.utils import util

import pandas as pd

import tensorflow as tf


class FlowersSource(Source):
    """Data Source for the TensorFlow flowers dataset.

    Provides function to read and preprocess the adult dataset.

    Attributes:
        categorical_features_list (list): List of category features
        quantitative_features_list (list): List of quantitative features
        target_feature (str): The target feature (column name)

    Args:
        filepath_test (str): Absolute path to the adult test dataset file.
        filepath_train (str): Absolute path to the adult train dataset file.
        skiprows (int, optional): Number of rows to skip.
    """
    def __init__(self, data_root,IMAGE_SHAPE):
        super().__init__()
        self.data_root = data_root
        self.IMAGE_SHAPE = IMAGE_SHAPE
        
    def read(self, force=False):
        """Read Adult dataset.

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            train and test data as pandas dataframe.

        Raises:
            IOError: if directory was not found
        """
        if not force and self.data is not None:
            return self.train_data, self.data

        path = self.data_root
        if not os.path.exists(path):
            raise IOError('Could not find the flower data.'
                          'File not found {}'.format(path))
        
        # tf hub expects intensity between [0-1]
        image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
        # keras interator
        image_data = image_generator.flow_from_directory(str(self.data_root), target_size=self.IMAGE_SHAPE)

        # for i, image_batch, label_batch in enumerate(image_data):
        #     if i == 0:
        #         image_batch_test = image_batch
        #         label_batch_test = label_batch
        #         continue

        #     image_batch_train = image_batch
        #     label_batch_train = label_batch
        return image_data
