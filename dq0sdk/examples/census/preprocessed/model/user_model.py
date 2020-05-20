# -*- coding: utf-8 -*-
"""Adult dataset example.

Neural network model definition

Example:
    >>> ./dq0 project create --name demo # doctest: +SKIP
    >>> cd demo # doctest: +SKIP
    >>> copy user_model.py to demo/model/ # doctest: +SKIP
    >>> ../dq0 data list # doctest: +SKIP
    >>> ../dq0 model attach --id <dataset id> # doctest: +SKIP
    >>> ../dq0 project deploy # doctest: +SKIP
    >>> ../dq0 model train # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP
    >>> ../dq0 model predict --input-path </path/to/numpy.npy> # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf import NeuralNetworkClassification

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """Derived from dq0sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        from sklearn.model_selection import train_test_split

        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        # read the dataset from the attached input source
        data = self.data_source.read()

        # do the train test split
        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data attributes
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(10, activation='tanh'),
            tf.keras.layers.Dense(10, activation='tanh'),
            tf.keras.layers.Dense(2, activation='softmax')])
        self.optimizer = 'Adam'
        self.learning_rate = 0.015

        self.epochs = 10
        self.num_microbatches = 250
        self.verbose = 0
        self.metrics = ['accuracy']

        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
