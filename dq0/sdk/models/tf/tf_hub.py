# -*- coding: utf-8 -*-
"""TF Hub pretrained Models

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.tf.neural_network_yaml import NeuralNetworkYaml
from dq0.sdk.models.yaml_configs.tf_hub_models import hub_models_dict

import tensorflow.compat.v1 as tf

logger = logging.getLogger()


class TFHub(NeuralNetworkYaml):
    """Tensorflow Hub Network Model.

    Uses NeuralNetworkYaml to read a TF Hub Yaml config
    to define the model.
    """

    def __init__(self, tf_hub_url=None):
        yaml_path = hub_models_dict[tf_hub_url]['yaml_path']
        super().__init__(yaml_path)
        self.task = hub_models_dict[tf_hub_url]['task']

        try:
            self.preprocessing = self.yaml_dict['PREPROCESSING']
        except Exception as e:
            fatal_error('PREPROCESSING is missinng in yaml: {}'.format(e), logger=logger)

    def setup_data(self, augment=False):
        """Setup Predefined data

        args:
            task (:obj:`str`): string specifying the task, i.e, im_clf or text_clf
            augment (bool): augment training data

        returns:
            X_train: true x or generator containing y
            y_train: true y or if x generator then None
            X_test: true x or generator containing y
            y_test: true y or if x generator then None
            fit_kwargs: steps_per_epoch and validation data if used
        """

        if len(self.data_sources) < 1:
            fatal_error('No data source found', logger=logger)

        source = next(iter(self.data_sources.values()))
        self.path_train = source.path_train
        self.path_test = source.path_test

        if self.task == 'im_clf':
            development_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],)
            development_generator = development_datagen.flow_from_directory(
                self.path_train,
                **self.preprocessing['development_dataflow'],
                **self.preprocessing['dataflow_kwargs'],)

            if augment:
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    **self.preprocessing['datagen_kwargs'],
                    **self.preprocessing['train_datagen'],)
            else:
                train_datagen = development_datagen
            train_generator = train_datagen.flow_from_directory(
                self.path_train,
                **self.preprocessing['train_dataflow'],
                **self.preprocessing['dataflow_kwargs'])

            test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],)
            test_generator = test_datagen.flow_from_directory(
                self.path_test,
                **self.preprocessing['test_dataflow'],
                **self.preprocessing['dataflow_kwargs'],)

            # Get number of batches per epoch
            steps_per_epoch = train_generator.samples // train_generator.batch_size
            validation_steps = development_generator.samples // development_generator.batch_size
            test_steps = test_generator.samples // test_generator.batch_size

            self.n_classes = train_generator.num_classes
            self.X_train = train_generator
            self.X_validate = development_generator
            self.X_test = test_generator

            self.fit_kwargs = dict(
                steps_per_epoch=steps_per_epoch,
                validation_data=development_generator,
                validation_steps=validation_steps)
            self.eval_train_kwargs = dict(steps=steps_per_epoch)
            self.eval_test_kwargs = dict(steps=test_steps)

            # set input/oupt size
            self.graph_dict['config']['layers'][-1]['config']['units'] = self.n_classes

        if self.task == 'text_clf':
            pass
