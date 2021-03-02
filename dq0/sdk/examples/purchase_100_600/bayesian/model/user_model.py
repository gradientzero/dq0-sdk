# -*- coding: utf-8 -*-
"""Purchase-100 from research dataset example.

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

from dq0.sdk.models.bayes.naive_bayesian_model import NaiveBayesianModel

from sklearn.naive_bayes import MultinomialNB

from tensorflow.keras import metrics

logger = logging.getLogger(__name__)


class UserModel(NaiveBayesianModel):
    """Derived from dq0.sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        # read the data via the attached input data source
        dataset = self.data_source.read()

        # do the train test split
        X_train_df, X_test_df, y_train_ts, y_test_ts = \
            (dataset.iloc[:10000, :-1],
            dataset.iloc[10000:, :-1],
            dataset.iloc[:10000, -1],
            dataset.iloc[10000:, -1],
            )

        # set data attributes
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

        logger.info('{}, {}'.format(self.X_train.shape, self.X_test.shape))

        self.input_dim = self.X_train.shape[1]
        self.output_dim = len(self.y_train.unique())

    def setup_model(self, **kwargs):
        """Setup model function

        Define the model here.
        """
        self._classifier_type = 'MultinomialNB'  # just for better-quality
        # printings

        self.model = MultinomialNB()

        self.metrics = ['accuracy']

        self.calibrate_posterior_probabilities = False

        print('Set up a ' + self._classifier_type + ' classifier.')
