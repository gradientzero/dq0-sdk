# -*- coding: utf-8 -*-
"""Estimator abstract base class

The Model class serves as the base class for all models.

Implementing subclasses have to define setup_data and setup_model functions.

Copyright 2021, Gradient Zero
All rights reserved
"""
import logging
import uuid

from dq0.sdk.estimators.data_handler.utils import data_handler_factory
from dq0.sdk.projects import Project

logger = logging.getLogger(__name__)


class Estimator(Project):
    """Abstract base class"""

    def __init__(self, data_source=None, log_key_string='', **kwargs):
        super().__init__()
        self.data_source = data_source
        self.uuid = uuid.uuid1()
        self.model = None
        self.log_key_string = log_key_string

    def setup_data(self, data_handler_instance='CSV', pipeline_steps=None, pipeline_config_path=None, transformers_root_dir='.', **kwargs):
        """Setup data function using a data_handler
        None of the estimators handle data by themselfs. They make use of predefined data_handler.
        It is selected by the 'data_handler_instance' attribute.

        Params:
            data_handler_instane: string: as defined in dq0.sdk.estimators.data_handler_utils; default is CSV
            **kwargs: open kwargs
        """
        self.data_handler = data_handler_factory(data_handler_instance, pipeline_steps=pipeline_steps, pipeline_config_path=pipeline_config_path,
                                                 transformers_root_dir=transformers_root_dir, log_key_string=self.log_key_string)
        self.X_train, self.X_test, self.y_train, self.y_test = self.data_handler.setup_data(self.data_source, **kwargs)

        return self.X_train, self.X_test, self.y_train, self.y_test

    def setup_model(self, **kwargs):
        """Setup model function."""
        pass

    def fit(self, X, y=None, **kwargs):
        """Model fit method"""
        if y is None:
            return self.model.fit(X, **kwargs)
        else:
            return self.model.fit(X, y, **kwargs)
