# -*- coding: utf-8 -*-
""" Sklearn ensemble models.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn import ensemble

from dq0.sdk.estimators.estimator import Estimator
from dq0.sdk.estimators.base_mixin import ClassifierMixin, RegressorMixin

logger = logging.getLogger(__name__)

# classification ensembles


class AdaBoostClassifier(ClassifierMixin, Estimator):
    def __init__(self, base_estimator=None, *, n_estimators=50, learning_rate=1.0, algorithm='SAMME.R', random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate, algorithm=algorithm,
                                                 random_state=random_state)


class BaggingClassifier(ClassifierMixin, Estimator):
    def __init__(self, base_estimator=None, n_estimators=10, *, max_samples=1.0, max_features=1.0, bootstrap=True, bootstrap_features=False, oob_score=False,
                 warm_start=False, n_jobs=None, random_state=None, verbose=0, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.BaggingClassifier(base_estimator=base_estimator, n_estimators=n_estimators, max_samples=max_samples, max_features=max_features,
                                                bootstrap=bootstrap, bootstrap_features=bootstrap_features, oob_score=oob_score, warm_start=warm_start,
                                                n_jobs=n_jobs, random_state=random_state, verbose=verbose)


class ExtraTreesClassifier(ClassifierMixin, Estimator):
    def __init__(self, n_estimators=100, *, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                 max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=False, oob_score=False, n_jobs=None,
                 random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.ExtraTreesClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                                   min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                   max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
                                                   min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs,
                                                   random_state=random_state, verbose=verbose, warm_start=warm_start, class_weight=class_weight,
                                                   ccp_alpha=ccp_alpha, max_samples=max_samples)


class GradientBoostingClassifier(ClassifierMixin, Estimator):
    def __init__(self, *, loss='deviance', learning_rate=0.1, n_estimators=100, subsample=1.0, criterion='friedman_mse', min_samples_split=2, 
                 min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3, min_impurity_decrease=0.0, min_impurity_split=None, init=None, 
                 random_state=None, max_features=None, verbose=0, max_leaf_nodes=None, warm_start=False, validation_fraction=0.1, n_iter_no_change=None,
                 tol=0.0001, ccp_alpha=0.0, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.GradientBoostingClassifier(loss=loss, learning_rate=learning_rate, n_estimators=n_estimators, subsample=subsample,
                                                         criterion=criterion, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                                         min_weight_fraction_leaf=min_weight_fraction_leaf, max_depth=max_depth, 
                                                         min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split, init=init,
                                                         random_state=random_state, max_features=max_features, verbose=verbose, max_leaf_nodes=max_leaf_nodes,
                                                         warm_start=warm_start, validation_fraction=validation_fraction, n_iter_no_change=n_iter_no_change,
                                                         tol=tol, ccp_alpha=ccp_alpha)


class RandomForestClassifier(ClassifierMixin, Estimator):
    def __init__(self, n_estimators=100, *, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                 max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False,
                 n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                                     min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                     max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
                                                     min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs,
                                                     random_state=random_state, verbose=verbose, warm_start=warm_start, class_weight=class_weight,
                                                     ccp_alpha=ccp_alpha, max_samples=max_samples)


# regression ensembles

class AdaBoostRegressor(RegressorMixin, Estimator):
    def __init__(self, base_estimator=None, *, n_estimators=50, learning_rate=1.0, loss='linear', random_state=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.AdaBoostRegressor(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate, loss=loss,
                                                random_state=random_state)


class BaggingRegressor(RegressorMixin, Estimator):
    def __init__(self, base_estimator=None, n_estimators=10, *, max_samples=1.0, max_features=1.0, bootstrap=True, bootstrap_features=False, oob_score=False,
                 warm_start=False, n_jobs=None, random_state=None, verbose=0, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.BaggingRegressor(base_estimator=base_estimator, n_estimators=n_estimators, max_samples=max_samples, max_features=max_features,
                                                bootstrap=bootstrap, bootstrap_features=bootstrap_features, oob_score=oob_score, warm_start=warm_start,
                                                n_jobs=n_jobs, random_state=random_state, verbose=verbose)


class ExtraTreesRegressor(RegressorMixin, Estimator):
    def __init__(self, n_estimators=100, *, criterion='mse', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                 max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=False, oob_score=False,
                 n_jobs=None, random_state=None, verbose=0, warm_start=False, ccp_alpha=0.0, max_samples=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.ExtraTreesRegressor(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                                  min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                  max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
                                                  min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs,
                                                  random_state=random_state, verbose=verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                                                  max_samples=max_samples)


class GradientBoostingRegressor(RegressorMixin, Estimator):
    def __init__(self, *, loss='ls', learning_rate=0.1, n_estimators=100, subsample=1.0, criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1,
                 min_weight_fraction_leaf=0.0, max_depth=3, min_impurity_decrease=0.0, min_impurity_split=None, init=None, random_state=None, max_features=None,
                 alpha=0.9, verbose=0, max_leaf_nodes=None, warm_start=False, validation_fraction=0.1, n_iter_no_change=None, tol=0.0001, ccp_alpha=0.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.GradientBoostingRegressor(loss=loss, learning_rate=learning_rate, n_estimators=n_estimators, subsample=subsample,
                                                        criterion=criterion, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                                        min_weight_fraction_leaf=min_weight_fraction_leaf, max_depth=max_depth,
                                                        min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split, init=init,
                                                        random_state=random_state, max_features=max_features, alpha=alpha, verbose=verbose,
                                                        max_leaf_nodes=max_leaf_nodes, warm_start=warm_start, validation_fraction=validation_fraction,
                                                        n_iter_no_change=n_iter_no_change, tol=tol, ccp_alpha=ccp_alpha)


class RandomForestRegressor(RegressorMixin, Estimator):
    def __init__(self, n_estimators=100, *, criterion='mse', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                 max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=None,
                 random_state=None, verbose=0, warm_start=False, ccp_alpha=0.0, max_samples=None, **kwargs):
        super().__init__(**kwargs)
        self.model_type = 'EnsembleEstimator'
        self.model = ensemble.RandomForestRegressor(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                                    min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                    max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
                                                    min_impurity_split=min_impurity_split, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs,
                                                    random_state=random_state, verbose=verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                                                    max_samples=max_samples)
