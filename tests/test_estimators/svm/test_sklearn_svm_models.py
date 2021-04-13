# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.estimators.SVM import sklearn_svm

import numpy as np

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.ones((4, 3))
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def test_SVC_001():
    X, y = get_data_int()
    estimator = sklearn_svm.SVC()
    estimator.fit(X, y)
    logger.debug("SVC.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("SVC.predict(): {}".format(estimator.predict(X)))
    logger.debug("SVC.score(): {}".format(estimator.score(X, y)))


def test_LinearSVC_001():
    X, y = get_data_int()
    estimator = sklearn_svm.LinearSVC()
    estimator.fit(X, y)
    logger.debug("LinearSVC.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LinearSVC.predict(): {}".format(estimator.predict(X)))
    logger.debug("LinearSVC.score(): {}".format(estimator.score(X, y)))


def test_NuSVC_001():
    X, y = get_data_int()
    estimator = sklearn_svm.NuSVC()
    estimator.fit(X, y)
    logger.debug("NuSVC.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("NuSVC.predict(): {}".format(estimator.predict(X)))
    logger.debug("NuSVC.score(): {}".format(estimator.score(X, y)))


def test_OneClassSVM_001():
    X, y = get_data_int()
    estimator = sklearn_svm.OneClassSVM()
    estimator.fit(X, y)
    logger.debug("OneClassSVM.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("OneClassSVM.predict(): {}".format(estimator.predict(X)))
    logger.debug("OneClassSVM.score(): {}".format(estimator.score(X, y)))


def test_SVR_001():
    X, y = get_data_int()
    estimator = sklearn_svm.SVR()
    estimator.fit(X, y)
    logger.debug("SVR.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("SVR.predict(): {}".format(estimator.predict(X)))
    logger.debug("SVR.score(): {}".format(estimator.score(X, y)))


def test_LinearSVR_001():
    X, y = get_data_int()
    estimator = sklearn_svm.LinearSVR()
    estimator.fit(X, y)
    logger.debug("LinearSVR.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("LinearSVR.predict(): {}".format(estimator.predict(X)))
    logger.debug("LinearSVR.score(): {}".format(estimator.score(X, y)))


def test_NuSVR_001():
    X, y = get_data_int()
    estimator = sklearn_svm.NuSVR()
    estimator.fit(X, y)
    logger.debug("NuSVR.predict_proba(): {}".format(estimator.predict_proba(X)))
    logger.debug("NuSVR.predict(): {}".format(estimator.predict(X)))
    logger.debug("NuSVR.score(): {}".format(estimator.score(X, y)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_SVC_001()
    test_LinearSVC_001()
    test_NuSVC_001()
    test_OneClassSVM_001()
    test_SVR_001()
    test_LinearSVR_001()
    test_NuSVR_001()
