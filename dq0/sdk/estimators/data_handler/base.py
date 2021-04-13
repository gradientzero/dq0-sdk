# -*- coding: utf-8 -*-
"""Base data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging
from abc import ABC

from dq0.sdk.pipeline.pipeline import Pipeline

logger = logging.getLogger(__name__)


class BasicDataHandler(ABC):
    """Basic Data Handler for all estimators"""

    def __init__(self, pipeline_steps=None, pipeline_config_path=None, transformers_root_dir='.', log_key_string=''):
        # Setup pipeline
        self.log_key_string = log_key_string
        if pipeline_steps is None and pipeline_config_path is None:
            self.pipeline = None
        else:
            self.pipeline = Pipeline(steps=pipeline_steps, config_path=pipeline_config_path, transformers_root_dir=transformers_root_dir,
                                     log_key_string=self.log_key_string)

    def setup_data(self, data_source, **kwargs):
        """ Empty setup data, just returns the data source
        """
        return data_source.read()
