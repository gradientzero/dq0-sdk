#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.cifar10_network import CIFAR10Model
import tensorflow as tf

logger = logging.getLogger()


class UserModel(CIFAR10Model):
    """Derived from dq0sdk.models.Model class
    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_selection = 'tf_tutorial'
        self.num_microbatches = 500

    def setup_model(self):
        """Setup model function

        Define the CIFAR CNN model.
        """

        self.learning_rate = 0.001  # 0.15
        self.epochs = 20
        self.verbose = 1
        self.metrics = ['accuracy']
        self.regularization_param = 0.0 #1e-3
        self.regularizer_dict = {
            'kernel_regularizer': tf.keras.regularizers.l2(
                self.regularization_param)  # ,
            # 'activity_regularizer': tf.keras.regularizers.l2(
            #    self.regularization_param),
            # 'bias_regularizer': tf.keras.regularizers.l2(
            #    self.regularization_param)
        }

        # network topology.
        # if self._classifier_type.startswith('DP-'):
        #    network_type = self._classifier_type[3:]
        # else:
        #    network_type = self._classifier_type
        # if util.case_insensitive_str_comparison(network_type, 'cnn'):
        print('Setting up a multilayer convolution neural network...')
        self.model = self._get_cnn_model(self._num_classes, self.model_selection)
