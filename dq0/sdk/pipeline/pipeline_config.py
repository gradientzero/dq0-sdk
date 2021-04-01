# -*- coding: utf-8 -*-
"""
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.pipeline import pipeline
from dq0.sdk.pipeline import transformer
import yaml
import os
import importlib
from dq0.mod_utils.modules import load_module, get_all_python_module_paths, read_module_content
import numpy as np

logger = logging.getLogger(__name__)


class PipelineConfig:
    """ Helper class to set up a pipline with a given config yaml. 
    """
    def __init__(self, config_path):
        self.config = self.read_from_yaml_file(config_path)

    def read_from_yaml_file(self, filename):
        """Reads metadata from the given yaml file.

        Args:
            filename: the path to the yaml file.
        """
        # check if file exists in current directory
        if not os.path.isfile(filename):
            raise FileNotFoundError('Could not find {}'.format(filename))

        with open(filename) as f:
            config = self.read_from_yaml(f)

        return config

    def read_from_yaml(self, yaml_input):
        """Reads metadata from the given yaml input.

        Args:
            yaml_input: open yaml file stream or yaml string.
        """
        config = yaml.load(yaml_input, Loader=yaml.FullLoader)
        return config

    def get_steps_from_config(self, root_dir='./dq0/sdk/pipeline/transformer/transformer.py'):
        """Goes though the list pipeline of the config and sets ups the setps list of tuples to initialize the pipeline with."""
        # TODO: root dir must be set correctly
        pipeline_config = self.config['pipeline']
        self.steps = []
        for key in pipeline_config:
            target_class = pipeline_config[key]['class']
            params = pipeline_config[key]
            # Try loading the class given the name in the pipeline and initialize with the params
            try:
                spec = importlib.util.spec_from_file_location(name=target_class,
                                                              location=root_dir)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                trans = getattr(module, target_class)(**params)
                if trans is None:
                    # TODO: add secure key
                    raise Exception(f"The transformer {target_class} couldn't be loaded")
                else:
                    self.steps.append((key, trans))

            except Exception as e:
                # TODO: add secure log key
                logging.debug(e)

        # TODO: add secure log key
        logger.info(f"loaded tranformers: {self.steps}")
        return self.steps