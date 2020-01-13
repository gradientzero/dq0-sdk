# -*- coding: utf-8 -*-
import yaml
import os

def get_config(path_to_yaml):
    """read yaml configuration file
    safe_load disallows objects but not sure what happens if it finds one
    """
    if not os.path.exists(path_to_yaml):
        print('file not found')
    else:
        print('loading yaml')
        with open(path_to_yaml, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    return config
