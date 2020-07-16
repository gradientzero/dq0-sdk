# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the bayesian census model locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0sdk
from dq0sdk.data.utils import util
from dq0sdk.examples.census.bayesian.model.user_model import UserModel

import tensorflow as tf
# At program startup, activate eager execution in order to call
# "tensor.numpy()" with Tf 1.0
tf.enable_eager_execution()

if __name__ == '__main__':

    print('\nRunning demo for the "Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '../_data/adult_with_rand_names.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
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

    # evaluate the model
    model.evaluate()
    model.evaluate(test_data=False)

    print('\nDemo run successfully!\n')
