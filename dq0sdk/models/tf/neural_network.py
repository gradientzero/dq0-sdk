# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

This can be used as a base class for UserModel definitions.

Example:
    ```python
    import dq0sdk.models.tf.NeuralNetwork

    class MyAwsomeModel(NeuralNetwork):
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
        myModel.fit()
        myModel.save()
    ```

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.models.model import Model

import tensorflow as tf
from tensorflow import keras


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.

    Note:
        fit, predict, and evaluate functions will be overriden at runtime
        when executed inside the DQ0 quarantine instance.

    Attributes:
        model_type (:obj:`str`): type of this model instance. Options: 'keras'.
        model_path (:obj:`str`): path of model (save / load)
        learning_rate (float): Learning rate for model fitting.
        epochs (int): Number of epochs for model fitting.
        num_microbatches (int): Number of microbatches in training.
        verbose (int): Set greater than 0 to print output.
        metrics (:obj:`list`): List of evaluation metrics.
        model (:obj:`tf.Keras.Sequential`): the actual keras model.
        X_train (:obj:`numpy.ndarray`): X training data
        y_train (:obj:`numpy.ndarray`): y training data
        X_test (:obj:`numpy.ndarray`, optional): X test data
        y_test (:obj:`numpy.ndarray`, optional): y test data
        input_dim (int): Number of input neurons.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'keras'
        self.learning_rate = 0.15
        self.epochs = 10
        self.num_microbatches = 250
        self.verbose = 0
        self.metrics = ['accuracy', 'mse']
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.input_dim = None

    def setup_data(self):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.
        """
        pass

    def setup_model(self):
        """Setup model function

        Implementing child classes can use this method to define the
        Keras model.
        """
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')]
        )

    def fit(self):
        """Model fit function.
        """
        optimizer = tf.keras.optimizers.SGD(learning_rate=self.learning_rate)
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=self.metrics)
        self.model.fit(self.X_train,
                       self.y_train,
                       epochs=self.epochs,
                       verbose=self.verbose)

    def predict(self, x):
        """Model predict function.

        Model scoring.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def evaluate(self, test_data=True, verbose=0):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Args:
            test_data (bool): False to use train data instead of test
                Default is True.
            verbose (int): Verbose level, Default is 0

        Returns:
            evaluation metrics
        """
        x = self.X_test if test_data else self.X_train
        y = self.y_test if test_data else self.y_train
        batch_size = self.num_microbatches
        num_minibatches = round(x.shape[0] / self.num_microbatches)
        x = x[:num_minibatches * self.num_microbatches]
        y = y[:num_minibatches * self.num_microbatches]
        return self.model.evaluate(
            x=x,
            y=y,
            batch_size=batch_size,
            verbose=verbose)

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model.save('{}/{}/{}.h5'.format(self.model_path, version, name),
                        include_optimizer=False)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        Args:
            name (:obj:`str`): The name of the model
            version (int): The version of the model
        """
        self.model = tf.keras.models.load_model(
            '{}/{}/{}.h5'.format(
                self.model_path, version, name),
            compile=False)
