# -*- coding: utf-8 -*-
"""Test excution script for Neural Network example.

This script is called from the command line to demonstrate the use of
the DQ0 SDK Neural Network model.

It loads data from the embedded adult dataset and trains and tests the
derived adult_dataset.neural_network model.

Example:
    python -m dq0sdk.examples.adult_dataset.run_example

:Authors:
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
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

    tr_dataset_df, test_dataset_df = dc.read()

    X_df, y_ts, num_tr_instances = dc.preprocess()

    model = NeuralNetwork_adult(model_path='notebooks/saved_model/')
    X_train_df, X_test_df, y_train_ts, y_test_ts =\
        model.setup_data(
            X_df,
            y_ts,
            dc.quantitative_features_list,
            num_tr_instances
        )

    model.setup_model()

    model.fit(X_train=X_train_df, y_train=y_train_ts)

    # model.fit_dp(X_train=X_train_df, y_train=y_train_ts)

    loss_tr, acc_tr, mse_te = model.evaluate(X_train_df, y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(X_test_df, y_test_ts)
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
