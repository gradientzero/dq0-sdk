# -*- coding: utf-8 -*-
"""Adult dataset example.

Neural network model definition

Example:
    >>> ./dq0 project create --name demo # doctest: +SKIP
    >>> cd demo # doctest: +SKIP
    >>> copy user_source.py to demo/data/ # doctest: +SKIP
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

from dq0sdk.models.tf.neural_network import NeuralNetwork

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    """Derived from dq0sdk.models.tf.NeuralNetwork class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (:obj:`str`): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attache data.
        """
        from sklearn.model_selection import train_test_split

        # read the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        column_names_list = [
            'lastname',
            'firstname',
            'age',
            'workclass',
            'fnlwgt',
            'education',
            'education-num',
            'marital-status',
            'occupation',
            'relationship',
            'race',
            'sex',
            'capital-gain',
            'capital-loss',
            'hours-per-week',
            'native-country',
            'income'
        ]

        dataset_df = self.data_source.read(
            names=column_names_list,
            sep=',',
            skiprows=self.skiprows,
            index_col=None,
            skipinitialspace=True,
            na_values={
                'capital-gain': 99999,
                'capital-loss': 99999,
                'hours-per-week': 99,
                'workclass': '?',
                'native-country': '?',
                'occupation': '?'}
        )

        target_feature = 'income'

        dataset_df.drop(['lastname', 'firstname'], axis=1, inplace=True)
        column_names_list.remove('lastname')
        column_names_list.remove('firstname')

        categorical_features_list = [
            col for col in dataset_df.columns
            if col != target_feature and dataset_df[col].dtype == 'object']

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        quantitative_features_list =\
            list(set(column_names_list) - set(categorical_features_list) - set(
                [target_feature]))

        dataset_df = self.prepare_data(
            dataset_df,
            categorical_features_list,
            quantitative_features_list,
            target_feature
        )

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(dataset_df.iloc[:, :-1],
                             dataset_df.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def prepare_data(self,
                     dataset_df,
                     categorical_features_list,
                     quantitative_features_list,
                     target_feature,
                     approach_for_missing_feature='imputation',
                     imputation_method_for_cat_feats='unknown',
                     imputation_method_for_quant_feats='median',
                     features_to_drop_list=None):
        """Helper function to prepare the data for training."""
        from dq0sdk.data.preprocessing import preprocessing
        import sklearn.preprocessing
        import pandas as pd

        # handle missing data
        dataset_df = preprocessing.handle_missing_data(
            dataset_df,
            mode=approach_for_missing_feature,
            imputation_method_for_cat_feats=imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=imputation_method_for_quant_feats,  # noqa: E501
            categorical_features_list=categorical_features_list,
            quantitative_features_list=quantitative_features_list)

        if features_to_drop_list is not None:
            dataset_df.drop(features_to_drop_list, axis=1, inplace=True)

        # Investigate whether ordinal features are present
        # (Weak) assumption: for each categorical feature, its values in the
        # test set is already present in the training set.
        dataset_df = pd.get_dummies(dataset_df, columns=categorical_features_list,
                                    dummy_na=False)
        # True => add a column to indicate NaNs. False => NaNs are ignored.
        # Rather than get_dummies, it would be better as follows ...
        # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # enc.fit(X_df[categorical_features_list])

        # Scale values to the range from 0 to 1 to be precessed by the neural network
        dataset_df[quantitative_features_list] =\
            sklearn.preprocessing.minmax_scale(
                dataset_df[quantitative_features_list])

        # label target
        y_ts = dataset_df[target_feature]
        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)
        dataset_df.drop([target_feature], axis=1, inplace=True)
        dataset_df[target_feature] = y_bin

        return dataset_df

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        from tensorflow import keras
        self.learning_rate = 0.3
        self.epochs = 5
        self.num_microbatches = 1
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
