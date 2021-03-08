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

    def __init__(self):
        super().__init__()
        self.data_source = None
        self.uuid = uuid.uuid1()
        self.model = None
    
    def setup_data(self, **kwargs):
        """Setup data function"""
        pass
    
    def setup_model(self, **kwargs):
        """Setup model function"""
        pass

    def fit(self, X, y=None, **kwargs):
        """Model fit method"""
        if y is None:
            return self.model.fit(X, **kwargs)
        else:
            return self.model.fit(X, y, **kwargs)

