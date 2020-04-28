# -*- coding: utf-8 -*-
"""Neural Network Model For Image Classification From Yaml

Basic tensorflow neural network implementation using Keras
for image classification using a yaml config

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import sys

from dq0sdk.models.model import Model
from dq0sdk.utils import YamlConfig
from dq0sdk.utils.managed_classes import custom_objects
from dq0sdk.utils.managed_classes import losses
from dq0sdk.utils.managed_classes import optimizers

import tensorflow.compat.v1 as tf

logger = logging.getLogger()


class NeuralNetworkYaml(Model):
    """Neural Network defined by Yaml file.

    Note:
        fit, predict, and evaluate functions will be overriden at runtime
        when executed inside the DQ0 quarantine instance.

    Args:
        model_path (:obj:`str`): path of model (save / load)
        yaml_path (:obj:`str`): path to the model definition file.

    Attributes:
        model_type (:obj:`str`): type of this model instance. Options: 'keras'.
        yaml_config (:obj:`dq0sdk.utils.YamlConfig`): yaml config reader
        yaml_dict (:obj:`dict`): Parsed yaml config dictionary.
        model_path (:obj:`str`): path of model (save / load)
        model (:obj:`tf.keras.Sequential`): the actual keras model.
        custom_objects (:obj:`dict`): A dictionary of additional model objects.

    """
    def __init__(self, model_path=None, yaml_path=None):
        super().__init__(model_path)
        self.model_type = 'keras'
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict

        self.model_path = model_path
        self.model = None
        self.custom_objects = custom_objects
        try:
            self.graph_dict = self.yaml_dict['MODEL']['GRAPH']
            self.optimizer_dict = self.yaml_dict['MODEL']['OPTIMIZER']
            self.dp_optimizer_dict = self.yaml_dict['MODEL']['DP_OPTIMIZER']
            self.loss_dict = self.yaml_dict['MODEL']['LOSS']
            self.metrics = self.yaml_dict['MODEL']['METRICS']

            self.epochs = self.yaml_dict['FIT']['epochs']
            self.dp_epochs = self.yaml_dict['FIT_DP']['epochs']
        except Exception as e:
            logger.error('YAML config is missing key {}'.format(e))
            sys.exit(1)

        try:
            self.optimizer = optimizers[self.optimizer_dict['optimizer']](**self.optimizer_dict['kwargs'])
            self.dp_optimizer = optimizers[self.dp_optimizer_dict['optimizer']](**self.dp_optimizer_dict['kwargs'])
            self.loss = losses[self.loss_dict['loss']](**self.loss_dict['kwargs'])
        except Exception as e:
            logger.error('optimizer or loss is not in managed list or specified in yaml {}'.format(e))
            sys.exit(1)

        try:
            self.fit_kwargs = self.yaml_dict['FIT']['kwargs']
        except Exception:
            self.fit_kwargs = {}
        try:
            self.fit_dp_kwargs = self.yaml_dict['FIT_DP']['kwargs']
        except Exception:
            self.fit_dp_kwargs = {}

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.eval_train_kwargs = {}
        self.eval_test_kwargs = {}

    def setup_data(self, augment=False):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            augment (bool): applies image augmenttion to training data
        """
        pass

    def setup_model(self):
        """Setup model from yaml MODEL

        This function converts the yaml MODEL:GRAPH: config
        to an instance of tf.keras.Sequential
        """
        if 'class_name' not in self.graph_dict.keys():
            self.graph_dict['class_name'] = 'Sequential'
        if 'name' not in self.graph_dict['config'].keys():
            self.graph_dict['config']['name'] = 'sequential'
        if 'keras_version' in self.graph_dict.keys():
            del self.graph_dict['keras_version']
        if 'backend' in self.graph_dict.keys():
            del self.graph_dict['backend']
        graph_str = self.yaml_config.dump_yaml(self.graph_dict)

        try:
            self.model = tf.keras.models.model_from_yaml(graph_str,
                                                      custom_objects=self.custom_objects)
        except Exception as e:
            logger.error('model_from_yaml: {}'.format(e))
            sys.exit(1)

    def fit(self):
        """Model fit function.

        Args:
            self.X_train: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or tf.keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights).
                A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.
                See https://www.tensorflow.org/api_docs/python/tf/keras/Model#evaluate
            self.y_train: Target data.
                Like the input data x, it could be either Numpy array(s) or TensorFlow tensor(s).
                It should be consistent with x (you cannot have Numpy inputs and tensor targets, or inversely).
                If x is a dataset, generator, or tf.keras.utils.Sequence instance, y should not be
                specified (since targets will be obtained from x).
        """
        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            self.X_train,
            self.y_train,
            epochs=self.epochs,
            **self.fit_kwargs,)

    def predict(self, x):
        """Model predict function.

        Model scoring.

        Args:
            x: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or tf.keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights).
                    A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.

        Returns:
            yhat: numerical matrix containing the predicted responses.

        TODO:
            add option to include class labels
        """
        return self.model.predict(x)

    def evaluate(self, test_data=True):
        """Model predict and evluate.

        Args:
            self.X_train/self.X_test: Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.
                A tf.data dataset. Should return a tuple of either (inputs, targets) or (inputs, targets, sample_weights).
                A generator or tf.keras.utils.Sequence returning (inputs, targets) or (inputs, targets, sample weights).
                A more detailed description of unpacking behavior for iterator types (Dataset, generator, Sequence) is given below.
                See https://www.tensorflow.org/api_docs/python/tf/keras/Model#evaluate
            self.y_train/self.y_test: Target data.
                Like the input data x, it could be either Numpy array(s) or TensorFlow tensor(s).
                It should be consistent with x (you cannot have Numpy inputs and tensor targets, or inversely).
                If x is a dataset, generator, or tf.keras.utils.Sequence instance, y should not be
                specified (since targets will be obtained from x).

        Returns:
            metrics: to be defined!

        """
        if test_data:
            evaluation = self.model.evaluate(
                self.X_test,
                self.y_test,
                **self.eval_test_kwargs,
            )
        else:
            evaluation = self.model.evaluate(
                self.X_train,
                self.y_train,
                **self.eval_train_kwargs,
            )
        return evaluation

    def run_all(self, augment=False):
        """Runs experiment

        Does all the setup data, model, fit and evaluate

        """
        # setup data
        self.setup_data(augment)

        # setup model
        self.setup_model()

        # fit
        self.fit()

        # evaluate
        evaluation = self.evaluate(test_data=False)
        for i, metric in enumerate(evaluation):
            if i == 0:
                print('Train loss: {}'.format(metric))
            else:
                print('Train {}: {}'.format(self.metrics[i - 1], metric))

        evaluation = self.evaluate()
        for i, metric in enumerate(evaluation):
            if i == 0:
                print('Test loss: {}'.format(metric))
            else:
                print('Test {}: {}'.format(self.metrics[i - 1], metric))

    def save(self, name='model', version=1):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model.save(
            '{}/{}/{}.h5'.format(
                self.model_path, version, name),
            include_optimizer=True)

    def load(self, name='model', version=1):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model = tf.keras.models.load_model(
            '{}/{}/{}.h5'.format(
                self.model_path, version, name),
            custom_objects=self.custom_objects,
            compile=True)

        if self.model.optimizer is None:
            self.model.compile(optimizer=self.dp_optimizer,
                               loss=self.loss,
                               metrics=self.metrics)
