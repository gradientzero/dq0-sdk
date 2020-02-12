# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

Todo:
    * Protect keras compile and fit functions

Example:
    class MyAwsomeModel(dq0.models.tf.NeuralNetwork):
        def init():
            self.learning_rate = 0.3

        def setup_data():
            # do something
            pass

        def setup_model():
            # freely deinfe the tf / keras model
            pass

    if __name__ == "__main__":
        myModel = MyAwsomeModel()
        myModel.setup_data()
        myModel.setup_model()
        # myModel.fit()
        myModel.fit_dp()
        myModel.save()


    ./dql-cli deploy-model --model-name

    ./dql-cli evalute-model --model-name
    return myModel.evalute()

    ./dql-cli model-predict --sdfsd
    return myModel.predict()

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

from dq0sdk.models.model import Model
from dq0sdk.utils.utils import custom_objects
from dq0sdk.utils.utils import YamlConfig

import os
import sys
import logging
from logging.config import fileConfig
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
import numpy as np

from tensorflow_privacy.privacy.optimizers import dp_optimizer


fileConfig(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../../logging.conf'))
logger = logging.getLogger('dq0')

class TFHub(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self, yaml_path=None, custom_objects=custom_objects()):
        super().__init__()
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict
        self.model_path = self.yaml_dict['MODEL_PATH']
        self.metrics = self.yaml_dict['METRICS']
        self.epochs = self.yaml_dict['FIT']['epochs']
        self.custom_objects = custom_objects
        self.model = None

        # Define loss
        self.loss = keras.losses.get(self.yaml_dict['LOSS']['class_name'])
        if len(self.yaml_dict['LOSS'].items()):
            loss_config = self.loss.get_config()
            for k,v in self.yaml_dict['LOSS'].items():
                if k in loss_config.keys():
                    loss_config[k] = v
        # print(loss_config)
        self.loss = self.loss.from_config(loss_config)
        
    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def setup_model(self):
        """Setup model from yaml MODEL
        
        This function converts the yaml MODEL: config
        to an instance of tf.Keras.Sequential
        """
        model_dict = self.yaml_dict['MODEL']
        if not 'class_name' in model_dict.keys():
            model_dict['class_name'] = 'Sequential'
        if not 'name' in model_dict['config'].keys():
            model_dict['config']['name'] = 'sequential'
        if 'keras_version' in model_dict.keys():
            del model_dict['keras_version']
        if 'backend' in model_dict.keys():
            del model_dict['backend']
        model_str = self.yaml_config.dump_yaml(model_dict)
        try:
            self.model = tf.keras.models.model_from_yaml(model_str,
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

    def fit(self, x, **kwargs):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            x: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights). 
                    A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        optimizer = tf.keras.optimizers.SGD(
            **self.yaml_dict['OPTIMIZER'])
        self.model.compile(optimizer=optimizer,
                           loss=self.loss,
                           metrics=self.metrics)
        
        self.model.fit(
            x=x,
            epochs=self.epochs, 
            **kwargs,
            )

    def fit_dp(self, x, **kwargs):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: discuss if we need both fit and fit_dp

        The implemented child class version will be final (non-derivable).

        Args:
            x: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights). 
                    A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.
            kwargs (:obj:`dict`): dictionary of optional arguments.
                Usually preprocessed data, feature columns etc.
        """
        optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
            **self.yaml_dict['DP_OPTIMIZER'])
        self.model.compile(optimizer=optimizer,
                           loss=self.loss,
                           metrics=self.metrics)
        
        self.model.fit(
            x=x,
            epochs=self.epochs,
            **kwargs,
            )
    
    def predict(self, x, **kwargs):
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
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def evaluate(self, x, **kwargs):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Args:
            x: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights). 
                    A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            metrics: to be defined!
        """
        evaluation = self.model.evaluate(x, **kwargs)
        return evaluation

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        self.model.save(
            '{}/{}_{}.h5'.format(
                self.model_path, name, version),
                include_optimizer=True)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """
        self.model = tf.keras.models.load_model(
            '{}/{}_{}.h5'.format(
                self.model_path, name, version),
                custom_objects=self.custom_objects,
                compile=True)

        if self.model.optimizer is None:
            optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
                **self.yaml_dict['DP_OPTIMIZER'])
            self.model.compile(optimizer=optimizer,
                               loss=self.loss,
                               metrics=self.metrics)
