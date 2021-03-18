# -*- coding: utf-8 -*-
""" Sklearn SVM models.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn import svm

from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import ClassifierMixin, RegressorMixin

logger = logging.getLogger(__name__)


# Classification SVMs
class SVC(ClassifierMixin, Estimator):
    def __init__(self, *, C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200,
                 class_weight=None, verbose=False, max_iter=- 1, decision_function_shape='ovr', break_ties=False, random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking, probability=probability, tol=tol,
                             cache_size=cache_size, class_weight=class_weight, verbose=verbose, max_iter=max_iter,
                             decision_function_shape=decision_function_shape, break_ties=break_ties, random_state=random_state)


class LinearSVC(ClassifierMixin, Estimator):

    def __init__(self, penalty='l2', loss='squared_hinge', *, dual=True, tol=0.0001, C=1.0, multi_class='ovr',
                 fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None, max_iter=1000, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.LinearSVC(penalty=penalty, loss=loss, dual=dual, tol=tol, C=C, multi_class=multi_class,
                                   fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight, verbose=verbose,
                                   random_state=random_state, max_iter=max_iter)


class NuSVC(ClassifierMixin, Estimator):

    def __init__(self, *, nu=0.5, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200,
                 class_weight=None, verbose=False, max_iter=- 1, decision_function_shape='ovr', break_ties=False, random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.NuSVC(nu=nu, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking, probability=probability, tol=tol,
                               cache_size=cache_size, class_weight=class_weight, verbose=verbose, max_iter=max_iter,
                               decision_function_shape=decision_function_shape, break_ties=break_ties , random_state=random_state)


class OneClassSVM(ClassifierMixin, Estimator):

    def __init__(self, *, kernel='rbf', degree=3, gamma='scale', coef0=0.0, tol=0.001, nu=0.5, shrinking=True, cache_size=200, verbose=False,
                 max_iter=- 1, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.OneClassSVM(kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, nu=nu, shrinking=shrinking, cache_size=cache_size,
                                     verbose=verbose, max_iter=- 1)


# Regression SVMs
class SVR(RegressorMixin, Estimator):
    def __init__(self, *, kernel='rbf', degree=3, gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200,
                 verbose=False, max_iter=- 1, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.SVR(kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, C=C, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size,
                             verbose=verbose, max_iter=max_iter)


class LinearSVR(RegressorMixin, Estimator):
    def __init__(self, *, epsilon=0.0, tol=0.0001, C=1.0, loss='epsilon_insensitive', fit_intercept=True, intercept_scaling=1.0, dual=True, verbose=0,
                 random_state=None, max_iter=1000, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.LinearSVR(epsilon=epsilon, tol=tol, C=C, loss=loss, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, dual=dual,
                                   verbose=0, random_state=None, max_iter=1000)


class NuSVR(RegressorMixin, Estimator):
    def __init__(self, *, nu=0.5, C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, tol=0.001, cache_size=200, verbose=False,
                 max_iter=- 1, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'SVMEstimator'
        self.model = svm.NuSVR(nu=nu, C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, shrinking=shrinking, tol=tol, cache_size=cache_size,
                                   verbose=verbose, max_iter=max_iter)
