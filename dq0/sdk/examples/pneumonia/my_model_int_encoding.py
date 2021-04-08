# -*- coding: utf-8 -*-
"""Neural Network model for Pneumonia image dataset.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.mod_utils.error import fatal_error
from dq0.sdk.models.tf import NeuralNetworkClassification

import tensorflow as tf


logger = logging.getLogger('dq0.' + __name__)


class UserModel(NeuralNetworkClassification):
    """CNN with pre-training"""

    def __init__(self):
        super().__init__()
        self._classifier_type = 'cnn'
        self.label_encoder = None
        logger.debug('Init user model done')

    def setup_data(self, **kwargs):
        # from sklearn.preprocessing import OneHotEncoder

        """Set up data function"""
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        logger.debug('Start Loading data')
        data = self.data_source.read()
        logger.debug('data.shape: {}'.format(data.shape))
        df_train = data[data['split'] == 'train']
        df_test = data[data['split'] == 'test']
        self.X_train = df_train.drop(['split', 'label'], axis=1).values
        self.y_train = ((df_train['label'] == 'pneumonial') * 1.).values  # .reshape(-1, 1)
        logger.debug('self.X_train.shape: {}'.format(self.X_train.shape))
        self.X_test = (df_test.drop(['split', 'label'], axis=1).values)
        self.y_test = ((df_test['label'] == 'pneumonial') * 1.).values  # .reshape(-1, 1)
        # lb = OneHotEncoder()
        # self.y_train  = lb.fit_transform(self.y_train).toarray()
        # self.y_test  = lb.transform(self.y_test).toarray()
        # for the model checker only; int encoding
        # self.y_train = np.argmax(self.y_train, axis=1)
        # self.y_test = np.argmax(self.y_test, axis=1)

        logger.debug("X_train.shape: {}".format(self.X_train.shape))
        logger.debug("X_test.shape: {}".format(self.X_test.shape))
        logger.debug("y_train.shape: {}".format(self.y_train.shape))
        logger.debug("y_test.shape: {}".format(self.y_test.shape))

        logger.debug("y_train: {}".format(self.y_train))
        logger.debug("y_train % 1s: {} %".format((100. * (sum(self.y_train)) / len(self.y_train))))

    def setup_model(self, **kwargs):
        """Set up model function"""
        # self.model = tf.keras.Sequential([hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4",
        #                                                 trainable=False, input_shape=(224, 224, 3)),
        #                                  tf.keras.layers.Dense(1, activation='linear')])
        self.model = tf.keras.Sequential([tf.keras.layers.Input(1280),
                                          tf.keras.layers.Dense(1280, activation='tanh'),
                                          tf.keras.layers.Dense(1280, activation='tanh'),
                                          tf.keras.layers.Dense(2, activation='softmax')])
        logger.debug('My model kwargs:{}'.format(kwargs))
        if 'epochs' in kwargs:
            try:
                self.epochs = int(kwargs['epochs'])
            except Exception as err:
                logger.info('Could not read the kwargs epochs, set epochs to default value, Error: {}'.format(err))
                self.epochs = 1
        else:
            self.epochs = 1

        self.optimizer = 'Adam'
        self.batch_size = 10
        self.metrics = ['accuracy', 'mae']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()

    def evaluate(self, test_data=True, verbose=0):
        from sklearn.metrics import confusion_matrix
        results = super().evaluate(test_data, verbose)

        if test_data:
            yhat = self.predict(self.X_test)
            cm = confusion_matrix(self.y_test, yhat)
        else:
            yhat = self.predict(self.X_train)
            cm = confusion_matrix(self.y_test, yhat)

        results['cm'] = cm
        # add comment
        return results
