# -*- coding: utf-8 -*-
""" Sklearn linear models.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn import linear_model

from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import ClassifierMixin, RegressorMixin

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
        self.model = linear_model.LogisticRegression(penalty=penalty, dual=dual, tol=tol,
                                                     C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling,
                                                     class_weight=class_weight, random_state=random_state, solver=solver,
                                                     max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                                                     warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)


class RidgeClassifier(ClassifierMixin, Estimator):
    """Sklearn RidgeClassifier"""

    def __init__(self, alpha=1.0, *, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, class_weight=None, solver='auto', 
                 random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = linear_model.RidgeClassifier(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, max_iter=max_iter, tol=tol, 
                                                  class_weight=class_weight, solver=solver, random_state=random_state)


class LinearRegression(RegressorMixin, Estimator):
    """Sklearn linear regression wrapper"""

    def __init__(self, *, fit_intercept=True, normalize=False, copy_X=True, n_jobs=None, positive=False, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = linear_model.LinearRegression(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs, positive=n_jobs)


class Ridge(RegressorMixin, Estimator):

    def __init__(self, alpha=1.0, *, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto', random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = linear_model.Ridge(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, max_iter=max_iter, tol=tol, solver=solver,
                                        random_state=None)


class Lasso(RegressorMixin, Estimator):

    def __init__(self, alpha=1.0, *, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False,
                 positive=False, random_state=None, selection='cyclic', **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = linear_model.Lasso(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, copy_X=copy_X, max_iter=max_iter, 
                                        tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)


class ElasticNet(RegressorMixin, Estimator):

    def __init__(self, alpha=1.0, *, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, max_iter=1000, copy_X=True, tol=0.0001, 
                 warm_start=False, positive=False, random_state=None, selection='cyclic', **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'LinearModelEstimator'
        self.model = linear_model.ElasticNet(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute,
                                             max_iter=max_iter, copy_X=copy_X, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, 
                                             selection=selection)
