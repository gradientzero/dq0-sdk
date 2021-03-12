# -*- coding: utf-8 -*-
"""Base tensorflow keras classes for all estimator subclasses

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
import uuid
from abc import abstractmethod
from dq0.sdk.estimators.estimator import Estimator
import numpy as np

logger = logging.getLogger(__name__)


class NeuralNetworkBase:
    """ Base TF Network mixin."""

    def fit(self, X, y, **kwargs):
        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)
        if 'epochs' in kwargs:
            epochs = kwargs.pop('epochs')
            self.model.fit(X, y, epochs=epochs, **kwargs)
        elif hasattr(self, epochs):
            self.model.fit(X, y, epochs=self.epochs, **kwargs)
        else:
            self.model.fit(X, y, **kwargs)

class NN_Classifier(NeuralNetworkBase):
    """Keras neural network classification models with one hot encoded targets."""

    def predict_proba(self, X):
        """Returns the """
        return self.model.predict(X)

    def predict(self, X):
        """Return the class as index on the one-hot-encoding format."""
        return np.argmax(self.model.predict(X), axis=-1)