# -*- coding: utf-8 -*-
"""
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from sklearn import pipeline
from dq0.sdk.pipeline import pipeline_config

from abc import abstractmethod, ABC
import sys
import pandas as pd

logger = logging.getLogger(__name__)


class Pipeline():

    def __init__(self, steps=None, config_path=None, **kwargs):
        """
        Initialize with steps directly (standalone mode) or with config file. Both can not be given.
        params:
            steps: List of (name, transform) tuples (implementing fit/transform) that are chained, in the order in which they are chained.
            config_path: path to config file where the pipelien steps are given.
        """
        if (steps is not None) and (config_path is None):
            self.pipeline = pipeline.Pipeline(steps)
        elif (steps is None) and (config_path is not None):
            pp_config = pipeline_config.PipelineConfig(config_path=config_path)
            steps = pp_config.get_steps_from_config()
            self.pipeline = pipeline.Pipeline(steps)
        else:
            logger.fatal("Both steps and config_path are given. Only one should be given.")
            sys.exit(1)

    def fit(self, X, y=None, **fit_params):
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None
        self.pipeline = self.pipeline.fit(X=X, y=y, **fit_params)

    def fit_transform(self, X, y=None, **fit_params):
        if hasattr(X, 'columns'):
            self.col_names = X.columns
        else:
            self.col_names = None
        X_t = self.pipeline.fit_transform(X=X, y=y, **fit_params)
        if self.col_names is not None:
            X_t = pd.DataFrame(X_t, columns=self.col_names)

        return X_t

    def get_params(self, deep=True):
        return self.pipeline.get_params(deep=deep)
