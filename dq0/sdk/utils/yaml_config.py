# -*- coding: utf-8 -*-
"""Process Yaml Config

Process yaml file to instantiate a basic tensorflow
neural network implementation using Keras.

Example:
    ```python
    if __name__ == "__main__":
        yaml_path = 'your path'
        model = MyAwesomeModel(yaml_path)
        model.setup_model()
    ```

Copyright 2020, Gradient Zero
All rights reserved
"""
import logging
import sys

from dq0.sdk.utils.managed_classes import custom_objects

import yaml

logger = logging.getLogger()


class YamlConfig():
    """Yaml parser for tf.keras models

    Yaml parser class for tf.Keras config files.
    """
    def __init__(self,
                 yaml_path,
                 yaml_dict=None,
                 custom_objects=custom_objects):
        self.yaml_str = None
        self.yaml_path = yaml_path
        self.custom_objects = custom_objects
        if yaml_dict is None:
            self.read_yaml_file()
        else:
            self.yaml_dict = yaml_dict

    def read_yaml_file(self):
        """Reads yaml file

        This function parses a yaml file to self.yaml_dict
        """
        try:
            with open(self.yaml_path, 'r') as yaml_file:
                self.yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)  # turnsout SafeLoader doesnt recognise !!python/tuple
        except Exception as e:
            logger.error('Could not find config at {}! {}'.format(self.yaml_path, e))
            sys.exit(1)
        return self.yaml_dict

    def save_yaml(self):
        """Save yaml dict to a yaml file"""
        try:
            with open(self.yaml_path, 'w') as yaml_file:
                yaml_file.write(self.yaml_dict)
        except Exception as e:
            logger.error('Cannot write yaml to {}! {}'.format(self.yaml_path, e))

    def dump_yaml(self, yaml_dict):
        self.yaml_str = yaml.dump(yaml_dict)
        return self.yaml_str
