# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.estimators.ensemble import sklearn_ensemble
import numpy as np

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.ones((4, 3))
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def test_AdaBoostClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.AdaBoostClassifier()
    estimator.fit(X, y)
    logger.debug("AdaBoostClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("AdaBoostClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("AdaBoostClassifier.score(): {}".format(estimator.score(X, y)))


def test_BaggingClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.BaggingClassifier()
    estimator.fit(X, y)
    logger.debug("BaggingClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("BaggingClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("BaggingClassifier.score(): {}".format(estimator.score(X, y)))


def test_ExtraTreesClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.ExtraTreesClassifier()
    estimator.fit(X, y)
    logger.debug("ExtraTreesClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("ExtraTreesClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("ExtraTreesClassifier.score(): {}".format(estimator.score(X, y)))


def test_GradientBoostingClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.GradientBoostingClassifier()
    estimator.fit(X, y)
    logger.debug("GradientBoostingClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("GradientBoostingClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("GradientBoostingClassifier.score(): {}".format(estimator.score(X, y)))


def test_RandomForestClassifier_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.RandomForestClassifier()
    estimator.fit(X, y)
    logger.debug("RandomForestClassifier.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("RandomForestClassifier.predict(): {}".format(estimator.predict(X)))
    logger.debug("RandomForestClassifier.score(): {}".format(estimator.score(X, y)))


def test_AdaBoostRegressor_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.AdaBoostRegressor()
    estimator.fit(X, y)
    logger.debug("AdaBoostRegressor.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("AdaBoostRegressor.predict(): {}".format(estimator.predict(X)))
    logger.debug("AdaBoostRegressor.score(): {}".format(estimator.score(X, y)))


def test_BaggingRegressor_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.BaggingRegressor()
    estimator.fit(X, y)
    logger.debug("BaggingRegressor.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("BaggingRegressor.predict(): {}".format(estimator.predict(X)))
    logger.debug("BaggingRegressor.score(): {}".format(estimator.score(X, y)))


def test_ExtraTreesRegressor_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.ExtraTreesRegressor()
    estimator.fit(X, y)
    logger.debug("ExtraTreesRegressor.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("ExtraTreesRegressor.predict(): {}".format(estimator.predict(X)))
    logger.debug("ExtraTreesRegressor.score(): {}".format(estimator.score(X, y)))


def test_GradientBoostingRegressor_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.GradientBoostingRegressor()
    estimator.fit(X, y)
    logger.debug("GradientBoostingRegressor.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("GradientBoostingRegressor.predict(): {}".format(estimator.predict(X)))
    logger.debug("GradientBoostingRegressor.score(): {}".format(estimator.score(X, y)))


def test_RandomForestRegressor_001():
    X, y = get_data_int()
    estimator = sklearn_ensemble.RandomForestRegressor()
    estimator.fit(X, y)
    logger.debug("RandomForestRegressor.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("RandomForestRegressor.predict(): {}".format(estimator.predict(X)))
    logger.debug("RandomForestRegressor.score(): {}".format(estimator.score(X, y)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_AdaBoostClassifier_001()
    test_BaggingClassifier_001()
    test_ExtraTreesClassifier_001()
    test_GradientBoostingClassifier_001
    test_RandomForestClassifier_001()
    test_AdaBoostRegressor_001()
    test_BaggingRegressor_001()
    test_ExtraTreesRegressor_001()
    test_GradientBoostingRegressor_001()
    test_RandomForestRegressor_001()
