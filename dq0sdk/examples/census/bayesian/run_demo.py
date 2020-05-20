# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the bayesian census model locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0sdk
from dq0sdk.examples.census.bayesian.model.user_model import UserModel

import numpy as np


if __name__ == '__main__':
    np.random.seed(seed=1)

    # input path
    path = '../_data/adult_with_rand_names.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init data source
    data_source = dq0sdk.data.text.CSV(filepath)

    # create model
    model = UserModel('notebooks/saved_model/')

    # attach data source
    model.attach_data_source(data_source)

    # prepare data
    model.setup_data()

    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate
    acc_tr = model.evaluate(test_data=False)
    acc_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
