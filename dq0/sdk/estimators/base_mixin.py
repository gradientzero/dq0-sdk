# -*- coding: utf-8 -*-
"""Base mixin classes for all estimator subclasses

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.estimators.estimator import Estimator # noqa

logger = logging.getLogger(__name__)


class ClassifierMixin:
    """Mixin class for all classifier estimators in DQ0"""

    def score(self, X, y, sample_weight=None):
        """Return the mean accuracy on the given test data and labels."""
        from sklearn.metrics import accuracy_score
        return accuracy_score(y, self.predict(X), sample_weight=sample_weight)

    def predict(self, X):
        """Predict classes for given dataset."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Get class probability for the given data X"""
        return self.model.predict(X)


class RegressorMixin:
    """Mixin class for all regressor estimators in DQ0"""

    def score(self, X, y, sample_weight=None):
        """Return the coefficient of determination :math:`R^2` of the
        prediction."""
        from sklearn.metrics import r2_score
        y_pred = self.predict(X)
        return r2_score(y, y_pred, sample_weight=sample_weight)

    def predict(self, X):
        """Predict for given dataset."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predict classes for given dataset."""
        return self.model.predict(X)


class ClusterMixin:
    """Mixin class for all cluster estimators in DQ0."""

    def fit_predict(self, X, y=None):
        self.fit(X)
        return self.labels_


class BiclusterMixin:
    """Mixin class for all bicluster estimators in DQ0."""

    def _do_something(self):
        """DO specific properties of bicluster estimators. TBD"""
        # TODO: define the Bin Cluster model base
        pass


class TransformerMixin:
    """Mininclass for all transformers in DQ0"""

    def fit_transform(self, X, y=None, **fit_params):
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)
