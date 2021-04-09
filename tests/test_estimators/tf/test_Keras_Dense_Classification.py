# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

import tensorflow as tf

from dq0.sdk.estimators.tf.keras_dense_classifier import (  # noqa
        Keras_Dense_Classifier_OHE, # noqa
        Keras_Dense_Classifier_Integer, # noqa
        Keras_Dense_Classifier_Binary) # noqa
from sklearn.preprocessing import OneHotEncoder # noqa

import numpy as np # noqa

logger = logging.getLogger(__name__)


def test_Keras_Dense_Classifier_ohe():

    X = tf.ones((4, 3))
    ohe = OneHotEncoder()
    y_int = np.array([[1], [2], [3], [4]])

    y = ohe.fit_transform(y_int).toarray()

    input_shape = (3,)
    n_classes = 4

    estimator = Keras_Dense_Classifier_OHE()
    estimator.setup_model(input_shape, n_classes, n_layers=[10, 10])
    estimator.fit(X, y, epochs=1)
    logger.debug("Keras_Dense_Classifier_OHE.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("Keras_Dense_Classifier_OHE.predict(): {}".format(estimator.predict(X)))
    logger.debug("Keras_Dense_Classifier_OHE.score(): {}".format(estimator.score(X, y_int)))


def test_Keras_Dense_Classifier_Integer():

    X = tf.ones((4, 3))
    y_int = np.array([1, 2, 3, 0])

    input_shape = (3,)
    n_classes = 4
    # The setup_model is executed in the init if all required parameters are given
    estimator = Keras_Dense_Classifier_Integer(input_shape=input_shape, n_classes=n_classes, n_layers=[10, 10])
    estimator.fit(X, y_int, epochs=1)
    logger.debug("Keras_Dense_Classifier_Integer.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("Keras_Dense_Classifier_Integer.predict(): {}".format(estimator.predict(X)))
    logger.debug("Keras_Dense_Classifier_Integer.score(): {}".format(estimator.score(X, y_int)))


def test_Keras_Dense_Classifier_Binary():

    X = tf.ones((4, 3))
    y_int = np.array([1, 0, 0, 1])
    input_shape = (3,)

    estimator = Keras_Dense_Classifier_Binary()
    estimator.setup_model(input_shape, n_layers=[10, 10])
    estimator.fit(X, y_int, epochs=1)
    logger.debug("Keras_Dense_Classifier_Binary.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("Keras_Dense_Classifier_Binary.predict(): {}".format(estimator.predict(X)))
    logger.debug("Keras_Dense_Classifier_Binary.score(): {}".format(estimator.score(X, y_int)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_Keras_Dense_Classifier_ohe()
    test_Keras_Dense_Classifier_Integer()
    test_Keras_Dense_Classifier_Binary()
