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
    Craig Lincoln <cl@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""
import logging
import os
import sys

from dq0sdk.models.model import Model
from dq0sdk.models.tf.tf_hub_models import hub_models_dict
from dq0sdk.utils.utils import YamlConfig
from dq0sdk.utils.utils import custom_objects

from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer

logger = logging.getLogger()


class TFHub(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self, model_path=None, tf_hub_url=None, custom_objects=custom_objects(), hub_models_dict=hub_models_dict):
        super().__init__(model_path)
        yaml_path = hub_models_dict[tf_hub_url]
        self.yaml_config = YamlConfig(yaml_path)
        self.yaml_dict = self.yaml_config.yaml_dict
        self.model = None
        self.model_path = model_path
        self.custom_objects = custom_objects
        self.n_classes = None
        
        self.optimizer = self.yaml_dict['OPTIMIZER']['optimizer'](**self.yaml_dict['OPTIMIZER']['kwargs'])
        self.dp_optimizer = self.yaml_dict['DP_OPTIMIZER']['optimizer'](**self.yaml_dict['DP_OPTIMIZER']['kwargs'])
        self.loss = self.yaml_dict['LOSS']['loss'](**self.yaml_dict['LOSS']['kwargs'])
        self.metrics = self.yaml_dict['METRICS']
        self.epochs = self.yaml_dict['FIT']['epochs']
        

    def setup_data(self):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        """
        pass

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

    def fit(self):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        TODO:
            train and validate need to be gotten from datasource
        """
        x = None

        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=x,
            epochs=self.epochs)

    def fit_dp(self):
        """Model fit function.

        Implementing child classes will perform model fitting here.

        This is the differential private training version.
        TODO: 
            discuss if we need both fit and fit_dp
            get train and validate from datasource

        The implemented child class version will be final (non-derivable).
        """
        x = None

        self.model.compile(optimizer=self.dp_optimizer,
                           loss=self.loss,
                           metrics=self.metrics)

        self.model.fit(
            x=x,
            epochs=self.epochs,
        )

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

        TODO:
            get test from data sources
        """
        x = None

        evaluation = self.model.evaluate(x)
        return evaluation

    def run_all(self):
        """Runs experiment
        
        Does all the setup data, model, fit and evaluate

        TODO:
            get train, validation and test
        """
        self.setup_data()
        self.setup_model()
        self.fit_dp()
        self.evaluate()

    def save(self):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        self.model.save(
            self.model_path,
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
            self.model_path,
            custom_objects=self.custom_objects,
            compile=True)

        if self.model.optimizer is None:
            self.model.compile(optimizer=self.dp_optimizer,
                               loss=self.loss,
                               metrics=self.metrics)

