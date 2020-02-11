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

import tensorflow as tf
from tensorflow import keras

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
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
        self.model = keras.Sequential([
            keras.layers.Input(len(kwargs['feature_columns'])),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')]
        )

    def prepare(self, **kwargs):
        """called before model fit on every run.

        Implementing child classes can use this method to prepare
        data for model training (preprocess data).

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def fit(self, **kwargs):
        """Model fit function.

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        X_train = self.X_train
        y_train = self.y_train

        optimizer = dp_optimizer.GradientDescentOptimizer(
            learning_rate=self.learning_rate)
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=self.metrics)
        self.model.fit(X_train,
                       y_train,
                       epochs=self.epochs,
                       verbose=self.verbose)

    def fit_dp(self, **kwargs):
        """Model fit with differential privacy.

        This method is final. Signature will be checked at runtime!

        Args:
            model (:obj:`keras.models.Model`): Keras model
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        X_train = self.X_train
        y_train = self.y_train

        # TODO: make training robust for any number of
        # minibatches -> bug in optimize function
        num_minibatches = round(X_train.shape[0] / self.num_microbatches)
        X_train = X_train[:num_minibatches * self.num_microbatches]
        y_train = y_train[:num_minibatches * self.num_microbatches]

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

        self.model.compile(optimizer=optimizer,
                           loss=loss,
                           metrics=self.metrics)

        self.model.fit(X_train,
                       y_train,
                       epochs=self.epochs,
                       verbose=self.verbose,
                       batch_size=self.num_microbatches)

    def predict(self, x, **kwargs):
        """Model predict function.

        Model scoring.

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            yhat: numerical matrix containing the predicted responses.
        """
        return self.model.predict(x)

    def evaluate(self, test_data=True, verbose=0, **kwargs):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Args:
            test_data (bool): False to use train data instead of test
                Default is True.
            verbose (int): Verbose level, Default is 0
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            metrics: to be defined!
        """
        x = self.X_test if test_data else self.X_train
        y = self.y_test if test_data else self.y_train
        batch_size = self.num_microbatches
        # TODO: SEE fit_dp: make training robust for any number of minibatches
        num_minibatches = round(x.shape[0] / self.num_microbatches)
        x = x[:num_minibatches * self.num_microbatches]
        y = y[:num_minibatches * self.num_microbatches]
        return self.model.evaluate(
            x=x,
            y=y,
            batch_size=batch_size,
            verbose=verbose)

    def save(self):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!
        """
        self.model.save('{}/{}.h5'.format(self.model_path, self.uuid),
                        include_optimizer=False)

    def load(self, name, version):
        """Loads the model.

        Load the model from local storage.

        This method is final. Signature will be checked at runtime!
        """
        self.model = tf.keras.models.load_model(
            '{}/{}.h5'.format(
                self.model_path, self.uuid),
            compile=False)
