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
import os
import sys

from dq0sdk.models.model import Model
from dq0sdk.utils.utils import YamlConfig
from dq0sdk.utils.utils import custom_objects

from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer

logger = logging.getLogger()


class NeuralNetworkYamlImageClassification(Model):
    def __init__(self, model_path=None, yaml_path=None, custom_objects=custom_objects()):
        super().__init__(model_path)
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict
        
        self.preprocessing = self.yaml_dict['PREPROCESSING']
        self.train_generator = None
        self.development_generator = None
        self.steps_per_epoch = None
        self.validation_steps = None
        self.test_generator = None
        self.test_steps = None

        self.model = None
        self.model_path = model_path
        self.custom_objects = custom_objects
        
        self.optimizer = self.yaml_dict['OPTIMIZER']['optimizer'](**self.yaml_dict['OPTIMIZER']['kwargs'])
        self.dp_optimizer = self.yaml_dict['DP_OPTIMIZER']['optimizer'](**self.yaml_dict['DP_OPTIMIZER']['kwargs'])
        self.loss = self.yaml_dict['LOSS']['loss'](**self.yaml_dict['LOSS']['kwargs'])
        self.metrics = self.yaml_dict['METRICS']
        self.epochs = self.yaml_dict['FIT']['epochs']

        self.test_data = True
        
    def setup_data(self, augmentation=False):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            augmentation (bool): applies image augmenttion to training data
        """
        self.path_train = list(self.data_sources.values())[0].path_train
        self.path_test = list(self.data_sources.values())[0].path_test

        development_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        development_generator = development_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['development_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        if augmentation:
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
        self.train_generator = train_generator
        self.development_generator = development_generator
        self.test_generator = test_generator
        self.steps_per_epoch = steps_per_epoch
        self.validation_steps = validation_steps
        self.test_steps = test_steps

    def setup_model(self):
        """Setup model from yaml MODEL

        This function converts the yaml MODEL: config
        to an instance of tf.Keras.Sequential
        """
        model_dict = self.yaml_dict['MODEL']
        if 'class_name' not in model_dict.keys():
            model_dict['class_name'] = 'Sequential'
        if 'name' not in model_dict['config'].keys():
            model_dict['config']['name'] = 'sequential'
        if 'keras_version' in model_dict.keys():
            del model_dict['keras_version']
        if 'backend' in model_dict.keys():
            del model_dict['backend']
        try:
            self.n_classes = list(self.data_sources.values())[0].n_classes
        except Exception as e:
            logger.error('Problem extracting n_classes from data sources: {}'.format(e))
            sys.exit(1)
            
        model_dict['config']['layers'][-1]['config']['units'] = self.n_classes

        model_str = self.yaml_config.dump_yaml(model_dict)
        
        try:
            self.model = keras.models.model_from_yaml(model_str,
                                                      custom_objects=self.custom_objects)
        except Exception as e:
            logger.error('model_from_yaml: {}'.format(e))
            sys.exit(1)
            
    def prepare(self, **kwargs):
        """called before model fit on every run.

        Implementing child classes can use this method to prepare
        data for model training (preprocess data).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def fit(self, epochs=None):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            epochs (int): number of epochs, default = from config
        """
        if epochs:
            self.epochs = epochs

        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=self.train_generator,
            steps_per_epoch=self.steps_per_epoch,
            validation_data=self.development_generator,
            validation_steps=self.validation_steps,
            epochs=self.epochs,)

    def fit_dp(self, epochs=None):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            epochs (int): number of epochs, default = from config
        """
        if epochs:
            self.epochs = epochs

        self.model.compile(optimizer=self.dp_optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=self.train_generator,
            steps_per_epoch=self.steps_per_epoch,
            validation_data=self.development_generator,
            validation_steps=self.validation_steps,
            epochs=self.epochs,)

    def predict(self, x):
        """Model predict function.

        Model scoring.

        This method is final. Signature will be checked at runtime!

        Args:
            x: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights).
                    A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.

        Returns:
            yhat: numerical matrix containing the predicted responses.

        TODO:
            add option to include class labels
        """
        return self.model.predict(x)

    def evaluate(self):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Returns:
            metrics: to be defined!

        """
        if self.test_data:
            evaluation = self.model.evaluate(x = self.test_generator,
                                            steps = self.test_steps)
        else:
            evaluation = self.model.evaluate(x = self.train_generator,
                                            steps = self.steps_per_epoch)
        return evaluation

    def run_all(self, augmentation=False, epochs=None):
        """Runs experiment
        
        Does all the setup data, model, fit and evaluate

        """
        # setup data
        self.setup_data(augmentation=augmentation)

        # setup model
        self.setup_model()

        # fit
        self.fit_dp(epochs=epochs)

        # evaluate
        self.test_data = False
        loss_tr, acc_tr, mse_tr = self.evaluate()
        self.test_data = True
        loss_te, acc_te, mse_te = self.evaluate()
        print('Train  Acc: %.2f %%' % (100 * acc_tr))
        print('Test  Acc: %.2f %%' % (100 * acc_te))

    def save(self):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        self.model.save(
            '{}/{}.h5'.format(
                self.model_path, self.uuid),
            include_optimizer=True)

    def load(self):
        """Loads the model.

        Load the model from local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """
        self.model = keras.models.load_model(
            '{}/{}.h5'.format(
                self.model_path, self.uuid),
            custom_objects=self.custom_objects,
            compile=True)

        if self.model.optimizer is None:
            self.model.compile(optimizer=self.dp_optimizer,
                               loss=self.loss,
                               metrics=self.metrics)
    
