# -*- coding: utf-8 -*-
"""Utils for data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

from dq0.sdk.estimators.data_handler.csv import CSVDataHandler

data_handler_types = {
    'csv': CSVDataHandler
}


def data_handler_factory(data_handler_instance, pipeline_steps=None, pipeline_config_path=None, transformers_root_dir='.'):
    data_handler_class = data_handler_types[data_handler_instance.lower()]
    return data_handler_class(pipeline_steps=pipeline_steps, pipeline_config_path=pipeline_config_path, transformers_root_dir=transformers_root_dir)
