# -*- coding: utf-8 -*-
"""Neural Network Model For Image Classification From Yaml

Basic tensorflow neural network implementation using Keras
for image classification using a yaml config

Todo:
    * Protect keras compile and fit functions

Example:


:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml

from tensorflow import keras

logger = logging.getLogger()


class NeuralNetworkYamlImageClassification(NeuralNetworkYaml):
    def __init__(self, model_path, yaml_path):
        super().__init__(model_path, yaml_path)
        self.preprocessing = self.yaml_dict['PREPROCESSING']
        self.augmentation = False

    def setup_data(self, augment=False):
        self.path_train = next(iter(self.data_sources.values())).path_train
        self.path_test = next(iter(self.data_sources.values())).path_test

        development_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        development_generator = development_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['development_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        if self.augmentation:
            train_datagen = keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],
                **self.preprocessing['train_datagen'],)
        else:
            train_datagen = development_datagen
        train_generator = train_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['train_dataflow'],
            **self.preprocessing['dataflow_kwargs'])

        test_datagen = keras.preprocessing.image.ImageDataGenerator(
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
