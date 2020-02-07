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
    # data paths.
    path = 'dq0sdk/data/adult/data/'
    path_test = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.test')
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.data')

    # init data sourcd
    dc = AdultSource(path_test, path_train)

    # create model
    model = NeuralNetwork_adult(model_path='notebooks/saved_model/')

    # attach data source
    model.attach_data_source(dc)

    # prepare data
    model.setup_data()

    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate
    loss_tr, acc_tr, mse_te = model.evaluate(test_data=False)
    loss_te, acc_te, mse_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
