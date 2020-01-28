#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult dataset example.
Run script.

@author: Wolfgang Gross <wg@gradient0.com>
"""

import os

from dq0sdk.data.adult import AdultSource
from dq0sdk.examples.adult_dataset.neural_network import NeuralNetwork_adult


if __name__ == '__main__':
    path = 'dq0sdk/data/adult/data/'
    path_test = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.test')
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.data')

    dc = AdultSource(path_test, path_train)
    train_data, data = dc.read()
    X_df, y_ts, num_tr_instances = dc.preprocess(
        approach_for_missing_feature='imputation',
        # 'imputation', 'dropping',
        imputation_method_for_cat_feats='unknown',
        # 'unknown', 'most_common_cat'
        imputation_method_for_quant_feats='median',  # 'median', 'mean'
        features_to_drop_list=None
    )

    model = NeuralNetwork_adult(model_path='notebooks/saved_model/')
    X_train_df, X_test_df, y_train_ts, y_test_ts = model.setup_data(
        X_df,
        y_ts,
        dc.quantitative_features_list,
        num_tr_instances
    )
    model.setup_model()
    model.fit(X_train=X_train_df, y_train=y_train_ts)
    loss_tr, acc_tr, mse_te = model.evaluate(X_train_df, y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(X_test_df, y_test_ts)
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
