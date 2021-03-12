# -*- coding: utf-8 -*-
"""Estimator abstract base class

The Model class serves as the base class for all models.

Implementing subclasses have to define setup_data and setup_model functions.

Copyright 2021, Gradient Zero
All rights reserved
"""
import logging
import uuid
from abc import abstractmethod
from dq0.sdk.projects import Project

logger = logging.getLogger(__name__)


class Estimator(Project):
    """Abstract base class"""

    def __init__(self, data_source=None, **kwargs):
        super().__init__()
        self.data_source = data_source
        self.uuid = uuid.uuid1()
        self.model = None

    def setup_data(self, **kwargs):
        """Setup data function"""
        if hasattr(self.data_source, 'feature_cols'):
            self.feature_cols = self.data_source.feature_cols
        if hasattr(self.data_source, 'target_cols'):
            self.target_cols = self.data_source.target_cols
        if hasattr(self.data_source, 'header'):
            data = self.data_source.read(names=self.data_source.header)
        else:
            data = self.data_source.read()
        return data
    
    def setup_model(self, **kwargs):
        """Setup model function"""
        pass

    def fit(self, X, y=None, **kwargs):
        """Model fit method"""
        if y is None:
            return self.model.fit(X, **kwargs)
        else:
            return self.model.fit(X, y, **kwargs)
