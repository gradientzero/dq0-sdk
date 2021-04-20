# -*- coding: utf-8 -*-
""" Diffprivlib linear models.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from diffprivlib.models import linear_regression, logistic_regression

from dq0.sdk.estimators.base_mixin import ClassifierMixin, RegressorMixin
from dq0.sdk.estimators.estimator import Estimator


logger = logging.getLogger(__name__)


class LogisticRegressionDP(ClassifierMixin, Estimator):
    """Diffprivlib logistic regression """

    def __init__(self, DP_epsilon=1, data_norm=None, tol=1e-4, C=1.0, fit_intercept=True, max_iter=100, verbose=0,
                 warm_start=False, n_jobs=None, accountant=None, **kwargs):
        """ Note the diff priv models are DP only. The target_epsilon value has to be set on initialize."""
        super().__init__(**kwargs)
        self.model_type = 'DPLinearModelEstimatorClassifier'
        self.model = logistic_regression.LogisticRegression(epsilon=DP_epsilon, data_norm=data_norm, tol=tol, C=C, fit_intercept=fit_intercept,
                                                            max_iter=max_iter, verbose=verbose, warm_start=warm_start, n_jobs=n_jobs, accountant=None)


class LinearRegressionDP(RegressorMixin, Estimator):
    """Diffprivlib linear regression """

    def __init__(self, DP_epsilon=1, bounds_X=None, bounds_y=None, fit_intercept=True, copy_X=True, accountant=None,
                 **kwargs):
        """ Note the diff priv models are DP only. The target_epsilon value has to be set on initialize."""
        super().__init__(**kwargs)
        self.model_type = 'DPLinearModelEstimatorRegressor'
        self.model = linear_regression.LinearRegression(epsilon=DP_epsilon, bounds_X=bounds_X, bounds_y=bounds_y, fit_intercept=fit_intercept,
                                                        copy_X=copy_X, accountant=accountant)
