# -*- coding: utf-8 -*-
"""TF Hub pretrained Models

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml
from dq0sdk.models.yaml_configs.tf_hub_models import hub_models_dict
from dq0sdk.utils.utils import custom_objects

logger = logging.getLogger()


class TFHub(NeuralNetworkYaml):
    def __init__(self, model_path=None, tf_hub_url=None, custom_objects=custom_objects()):
        yaml_path = hub_models_dict[tf_hub_url]
        super().__init__(model_path, yaml_path)
