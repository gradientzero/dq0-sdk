# -*- coding: utf-8 -*-
"""Adult dataset example.

Neural network model definition

Example:
    ```bash
    ./dq0 project create --name demo
    cd demo
    copy user_source.py to demo/data/
    copy user_model.py to demo/model/
    ../dq0 data list
    ../dq0 model attach --id <dataset id>
    ../dq0 project deploy
    ../dq0 model train
    ../dq0 model state
    ../dq0 model predict --input-path </path/to/numpy.npy>
    ../dq0 model state
    ```

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.neural_network import NeuralNetwork

logger = logging.getLogger()


class UserModel(NeuralNetwork):
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
        """
        from sklearn.model_selection import train_test_split

        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        data = source.read()

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        from tensorflow import keras
        self.learning_rate = 0.3
        self.epochs = 5
        self.num_microbatches = 1
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
