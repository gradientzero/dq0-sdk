# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.estimators.linear_model import sklearn_lm
import numpy as np

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.ones((4, 3))
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def test_LogisticRegression_001():
    X, y = get_data_int()
    estimator = sklearn_lm.LogisticRegression()
    estimator.fit(X, y)
    logger.debug("LogisticRegression.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LogisticRegression.predict(): {}".format(estimator.predict(X)))
    logger.debug("LogisticRegression.score(): {}".format(estimator.score(X, y)))


def test_RidgeClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_lm.RidgeClassifier()
    estimator.fit(X, y)
    logger.debug("RidgeClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("RidgeClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("RidgeClassifier.score(): {}".format(estimator.score(X, y)))


def test_LinearRegression_001():
    X, y = get_data_int()
    estimator = sklearn_lm.LinearRegression()
    estimator.fit(X, y)
    logger.debug("LinearRegression.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LinearRegression.predict(): {}".format(estimator.predict(X)))
    logger.debug("LinearRegression.score(): {}".format(estimator.score(X, y)))


def test_Ridge_001():
    X, y = get_data_int()
    estimator = sklearn_lm.Ridge()
    estimator.fit(X, y)
    logger.debug("Ridge.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("Ridge.predict(): {}".format(estimator.predict(X)))
    logger.debug("Ridge.score(): {}".format(estimator.score(X, y)))


def test_Lasso_001():
    X, y = get_data_int()
    estimator = sklearn_lm.Lasso()
    estimator.fit(X, y)
    logger.debug("Lasso.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("Lasso.predict(): {}".format(estimator.predict(X)))
    logger.debug("Lasso.score(): {}".format(estimator.score(X, y)))


def test_ElasticNet_001():
    X, y = get_data_int()
    estimator = sklearn_lm.ElasticNet()
    estimator.fit(X, y)
    logger.debug("ElasticNet.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("ElasticNet.predict(): {}".format(estimator.predict(X)))
    logger.debug("ElasticNet.score(): {}".format(estimator.score(X, y)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_LogisticRegression_001()
    test_RidgeClassifier_001()
    test_LinearRegression_001()
    test_Ridge_001()
    test_Lasso_001()
    test_ElasticNet_001()