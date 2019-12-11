# -*- coding: utf-8 -*-
"""Neural Network Model

Basic tensorflow neural network implementation using Keras.

Todo:
    * Implement load, save, predict, and evaluate
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
"""

from dq0.models.model import Model

import tensorflow as tf
from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self):
        super().__init__()
        self.learning_rate = 0.15
        self.epochs = 10
        self.num_microbatches = 250
        self.metrics = ['accuracy', 'mse']
        # Range possible: grid search, all combinations inside range

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def setup_model(self, **kwargs):
        """Setup model function

        Implementing child classes can use this method to define the
        Keras model.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        model = keras.Sequential([
            keras.layers.Input(len(kwargs['feature_columns'])),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')]
        )
        return model

    def prepare(self, **kwargs):
        """called before model fit on every run.

        Implementing child classes can use this method to prepare
        data for model training (preprocess data).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def fit(self, model, **kwargs):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            model (:obj:`keras.models.Model`): Keras model
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        preprocessed_data = kwargs['preprocessed_data']
        feature_columns = kwargs['feature_columns']
        target_column = kwargs['target_column']

        optimizer = dp_optimizer.GradientDescentOptimizer(
            learning_rate=self.learning_rate)
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        model.compile(optimizer=optimizer, loss=loss, metrics=self.metrics)
        model.fit(preprocessed_data[feature_columns],
                  preprocessed_data[target_column],
                  epochs=self.epochs,
                  verbose=0)

    def fit_dp(self, model, **kwargs):
        """Model fit with differential privacy.

        This method is final. Signature will be checked at runtime!

        Args:
            model (:obj:`keras.models.Model`): Keras model
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        preprocessed_data = kwargs['preprocessed_data']
        feature_columns = kwargs['feature_columns']
        target_column = kwargs['target_column']

        # DPSGD Training
        optimizer = dp_optimizer.DPGradientDescentGaussianOptimizer(
            l2_norm_clip=1.0,
            noise_multiplier=1.1,
            num_microbatches=self.num_microbatches,
            learning_rate=self.learning_rate)

        # Compute vector of per-example loss rather than
        # its mean over a minibatch.
        loss = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True,
            reduction=tf.compat.v1.losses.Reduction.NONE)

        model.compile(optimizer=optimizer, loss=loss, metrics=self.metrics)

        model.fit(preprocessed_data[feature_columns],
                  preprocessed_data[target_column],
                  epochs=10,
                  verbose=0,
                  batch_size=250)

    def predict(self, **kwargs):
        """Model predict function.

        Model scoring.

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        pass

    def evaluate(self, **kwargs):
        """Model predict and evluate.

        TODO: define returned metrics

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            metrics: to be defined!
        """
        pass

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        pass

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name of the model to load
            version (str): version of the model to load
        """
        pass
