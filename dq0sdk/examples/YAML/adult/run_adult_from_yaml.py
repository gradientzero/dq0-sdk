#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yaml model example.

@author: Craig Lincoln <cl@gradient0.com>
"""

import logging
import os

from dq0sdk.data.adult import AdultSource
from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml

import pandas as pd

import sklearn
import sklearn.preprocessing

logger = logging.getLogger()


class NeuralNetworkYamlAdult(NeuralNetworkYaml):
    def __init__(self, yaml_path):
        super().__init__(yaml_path)
        self.input_dim = None

    def setup_data(self, X_df, y_ts, quantitative_features_list, num_tr_instances):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        train_data, data = source.read()

        # preprocess data
        X_df, y_ts, num_tr_instances = source.preprocess(
            approach_for_missing_feature='imputation',
            # 'imputation', 'dropping',
            imputation_method_for_cat_feats='unknown',
            # 'unknown', 'most_common_cat'
            imputation_method_for_quant_feats='median',  # 'median', 'mean'
            features_to_drop_list=None
        )

        # Scale values to the range from 0 to 1; to be precessed by the neural network
        X_df[quantitative_features_list] = sklearn.preprocessing.minmax_scale(X_df[quantitative_features_list])

        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)  # test to label
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)

        X_train_df, X_test_df, y_train_ts, y_test_ts = preprocessing.train_test_split(X_df, y_bin, num_tr_instances)
        self.input_dim = X_train_df.shape[1]

        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts


if __name__ == '__main__':
    # data paths.
    path = 'dq0sdk/data/adult/data/'
    path_test = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../../', path, 'adult.test')
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../../', path, 'adult.data')

    # create data source
    dc = AdultSource(path_test, path_train)

    # create model
    yaml_path = 'dq0sdk/examples/yaml/adult/yaml_config_adult.yaml'
    model = NeuralNetworkYamlAdult(yaml_path=yaml_path)

    # attach data source
    model.attach_data_source(dc)

    # setup data
    model.setup_data()

    # setup model
    model.setup_model()

    # fit model
    model.fit()

    # evaluate
    loss_tr, acc_tr, mse_te = model.evaluate(test_data=False)
    loss_te, acc_te, mse_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))

    # DP Version
    model.fit_dp()

    # evaluate
    loss_tr, acc_tr, mse_te = model.evaluate(test_data=False)
    loss_te, acc_te, mse_te = model.evaluate()
    print('Train DP Acc: %.2f %%' % (100 * acc_tr))
    print('Test DP  Acc: %.2f %%' % (100 * acc_te))
