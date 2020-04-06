#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Model template

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.image_cnn import ImageCNN

logger = logging.getLogger()


class UserModel(ImageCNN):
    """Derived dq0sdk.models.tf.image_cnn.ImageCNN class

    Just a wrapper
    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
