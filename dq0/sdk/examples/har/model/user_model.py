# -*- coding: utf-8 -*-
"""Human Activity Recognition dataset example.

http://groupware.les.inf.puc-rio.br/har

Ugulino, W.; Cardador, D.; Vega, K.; Velloso, E.; Milidiu, R.; Fuks, H. Wearable Computing: Accelerometers' Data Classification of Body Postures and Movements. Proceedings of 21st Brazilian Symposium on Artificial Intelligence. Advances in Artificial Intelligence - SBIA 2012. In: Lecture Notes in Computer Science. , pp. 52-61. Curitiba, PR: Springer Berlin / Heidelberg, 2012. ISBN 978-3-642-34458-9. DOI: 10.1007/978-3-642-34459-6_6.

Read more: http://groupware.les.inf.puc-rio.br/har#ixzz6bPytcguP

Neural network model definition

Example:
    >>> ./dq0 project create --name demo # doctest: +SKIP
    >>> cd demo # doctest: +SKIP
    >>> copy user_model.py to demo/model/ # doctest: +SKIP
    >>> ../dq0 data list # doctest: +SKIP
    >>> ../dq0 model attach --id <dataset id> # doctest: +SKIP
    >>> ../dq0 project deploy # doctest: +SKIP
    >>> ../dq0 model train # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP
    >>> ../dq0 model predict --input-path </path/to/numpy.npy> # doctest: +SKIP
    >>> ../dq0 model state # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.models.tf import NeuralNetworkClassification

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """Derived from dq0.sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.
    """

    def __init__(self):
        super().__init__()

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        from sklearn.model_selection import train_test_split

        # read and preprocess the data
        dataset_df = self.preprocess()

        # do the train test split
        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(dataset_df.iloc[:, :-1],
                             dataset_df.iloc[:, -1],
                             test_size=500,
                             train_size=500,
                             stratify=dataset_df.iloc[:, -1])

        # set data attributes
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

        self.input_dim = self.X_train.shape[1]
        self.output_dim = len(self.y_train.unique())
        

    def preprocess(self):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        import sklearn.preprocessing
        import pandas as pd

        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        # read the data via the attached input data source
        dataset = self.data_source.read(
            sep=';',
            decimal=',',
        )

        X = dataset.drop('class', axis=1).copy()
        y = dataset['class']

        # Convert cat to dummies
        dtypes = X.dtypes
        cat_cals = dtypes.loc[dtypes=='O'].index

        for col in cat_cals:
            X = X.join(pd.get_dummies(X[col], drop_first=True))
            X.drop(col, axis=1, inplace=True)

        # LE class
        y = sklearn.preprocessing.LabelEncoder().fit_transform(y)

        dataset = pd.concat([X, pd.Series(y)], axis=1)

        return dataset

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        import tensorflow.compat.v1 as tf

        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(self.input_dim),
            tf.keras.layers.Dense(int(0.8 * self.input_dim), activation='relu'),
            # tf.keras.layers.Dense(int(0.8 * self.input_dim), activation='relu'),
            # tf.keras.layers.Dense(int(0.8 * self.input_dim), activation='relu'),
            tf.keras.layers.Dense(self.output_dim, activation='softmax')])
        self.optimizer = 'Adam'
        # To set optimizer params, self.optimizer = optimizer instance
        # rather than string, with params values passed as input to the class
        # constructor. E.g.:
        #
        #   import tensorflow
        #   self.optimizer = tensorflow.keras.optimizers.Adam(
        #       learning_rate=0.015)
        #
        self.epochs = 1000
        self.batch_size = 250
        self.metrics = ['accuracy']
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy()
        # As an alternative, define the loss function with a string
