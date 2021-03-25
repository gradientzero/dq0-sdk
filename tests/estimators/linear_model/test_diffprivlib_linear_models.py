# -*- coding: utf-8 -*-
""" 
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.estimators.linear_model import diffprivlib_lm
import numpy as np

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.ones((4, 3))
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def test_LogisticRegression_001():
    X, y = get_data_int()
    estimator = diffprivlib_lm.LogisticRegression()
    estimator.fit(X, y)
    logger.debug("LogisticRegression.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LogisticRegression.predict(): {}".format(estimator.predict(X)))
    logger.debug("LogisticRegression.score(): {}".format(estimator.score(X, y)))


def test_LinearRegression_001():
    X, y = get_data_int()
    estimator = diffprivlib_lm.LinearRegression()
    estimator.fit(X, y)
    logger.debug("LinearRegression.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LinearRegression.predict(): {}".format(estimator.predict(X)))
    logger.debug("LinearRegression.score(): {}".format(estimator.score(X, y)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_LogisticRegression_001()
    test_LinearRegression_001()
