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
import tensorflow_hub as hub
from tensorflow import keras
import numpy as np
np.random.seed(1)

from tensorflow_privacy.privacy.optimizers import dp_optimizer


class TFHub(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self, kwargs):
        super().__init__()
        self.tf_url=kwargs['hub_layer_kwargs']['tf_url']
        self.trainable=kwargs['hub_layer_kwargs']['trainable'] # default False
        self.optional_hub_layer_kwargs=kwargs['hub_layer_kwargs']['optional']
        self.keras_layers = kwargs['lst_tf_keras_layers']
        self.optimizer = kwargs['optimizer']['optimizer']
        self.loss = kwargs['optimizer']['loss']
        self.metrics = kwargs['optimizer']['metrics']
        self.epochs = kwargs['model.fit']['epochs']
        self.train_generator = kwargs['train_generator']
        self.development_generator = kwargs['development_generator']
        self.test_generator = kwargs['test_generator']
        self.model_path = kwargs['model_path']
        # stuff to do with dp training
        self.learning_rate=0.15
        self.num_microbatches = 250
        self.verbose = 0
        self.metrics = ['accuracy', 'mse']
        self.model = None
        
        # Range possible: grid search, all combinations inside range

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used by child classes to prepare data or perform
        other tasks that dont need to be repeated for every training run.

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
        """
        pass

    def setup_model(self):
        """retrieve tensorflow hub model for use in setup_model
        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments
            kwargs['trainable'] (bool): True to unfreeze weights, default False
            kwargs['arguments'] (dict): optionally, a dict with additional keyword arguments passed to the callable. 
                                        These must be JSON-serializable to save the Keras config of this layer.
                                        eg dict(batch_norm_momentum=0.997)
            **kwargs: 'output_shape': A tuple with the (possibly partial) output shape of the callable without 
                      leading batch size. Other arguments are pass into the Layer constructor.
        """
        hub_layer = hub.KerasLayer(self.tf_url,
                                   trainable=self.trainable,
                                   **self.optional_hub_layer_kwargs)
        
        self.model=tf.keras.Sequential([hub_layer])
        # self.model.add(self.keras_layers)
        self.model.add(tf.keras.layers.Dropout(rate=0.2))
        self.model.add(tf.keras.layers.Dense(
                         self.train_generator.num_classes,
                         activation='softmax',
                         kernel_regularizer=tf.keras.regularizers.l2(0.0001)))
        
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

        self.model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.005, momentum=0.9),
                           loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1),
                           metrics=['accuracy'])
        
        steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        validation_steps = self.development_generator.samples // self.development_generator.batch_size
        print([steps_per_epoch,validation_steps])
        hist = self.model.fit(
            self.train_generator,
            epochs=self.epochs, 
            steps_per_epoch=steps_per_epoch,
            validation_data=self.development_generator,
            validation_steps=validation_steps).history
        
    def fit_dp(self, **kwargs):
        """Model fit with differential privacy.

        This method is final. Signature will be checked at runtime!

        Args:
            model (:obj:`keras.models.Model`): Keras model
            kwargs (:obj:`dict`): dictionary of optional arguments.
                preprocessed data, feature columns
        """
        # TODO: overwrite keras 'compile' and 'fit' at runtime!!!
        X_train = kwargs['X_train']
        y_train = kwargs['y_train']

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

    def evaluate(self, **kwargs):
        """Model predict and evluate.

        This method is final. Signature will be checked at runtime!

        Args:
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            metrics: to be defined!
        """
        test_steps = self.test_generator.samples // self.test_generator.batch_size
        evaluation = self.model.evaluate(self.test_generator,steps = test_steps)
        return evaluation

    def save(self, name, version):
        """Saves the model.

        Save the model in binary format on local storage.

        This method is final. Signature will be checked at runtime!

        Args:
            name (str): name for the model to use for saving
            version (str): version of the model to use for saving
        """
        self.model.save('{}/{}_{}.h5'.format(self.model_path, name, version),
                        include_optimizer=False)

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
                self.model_path, name, version), compile=False)
