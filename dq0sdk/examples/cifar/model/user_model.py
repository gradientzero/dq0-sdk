# -*- coding: utf-8 -*-
"""Neural Network model for CIFAR10 dataset.

Use this example to train a classifier on the CIFAR10 image data.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.image_cnn import ImageCNN

logger = logging.getLogger()


class UserModel(ImageCNN):
    """Convolutional Neural Network model implementation for Cifar10.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_model(self):
        """Setup model function
        """
        super().setup_model()

        self.learning_rate = 0.001  # 0.15
        self.epochs = 50  # 50 in ML-leaks paper

    def setup_data(self):
        """Setup data function
        """
        super().setup_data()

        print('\nAttached train dataset to user model. Feature matrix '
              'shape:',
              self.X_train.shape)
        print('Class-labels vector shape:', self.y_train.shape)

        if self.X_test is not None:
            logger.debug('\nAttached test dataset to user model. Feature matrix '
                         'shape:', self.X_test.shape)
        if self.y_test is not None:
            logger.debug('Class-labels vector shape:', self.y_test.shape)
