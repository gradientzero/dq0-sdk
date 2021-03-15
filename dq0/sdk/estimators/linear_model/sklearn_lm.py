# -*- coding: utf-8 -*-
""" Keras dense neural network for classification with different target encoding.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn.linear_model import LogisticRegression as SKlearnLogisticRegression

from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import ClassifierMixin

logger = logging.getLogger(__name__)


class LogisticRegression(ClassifierMixin, Estimator):
    """Sklearn logistic regression wrapper"""

    def __init__(self, penalty='l2', *, dual=False, tol=0.0001,
                 C=1.0, fit_intercept=True, intercept_scaling=1,
                 class_weight=None, random_state=None,
                 solver='lbfgs', max_iter=100, multi_class='auto',
                 verbose=0, warm_start=False, n_jobs=None, l1_ratio=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = SKlearnLogisticRegression(penalty=penalty, dual=dual, tol=tol,
                                               C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling,
                                               class_weight=class_weight, random_state=random_state, solver=solver,
                                               max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                                               warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
