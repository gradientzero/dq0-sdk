# -*- coding: utf-8 -*-
"""20 Newsgroups dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""
import os

import dq0.sdk
from dq0.sdk.data.utils import util
from dq0.sdk.examples.newsgroups.bayesian.model.user_model import UserModel

import tensorflow as tf
# At program startup, activate eager execution in order to call
# "tensor.numpy()" with Tf 1.0
tf.compat.v1.enable_eager_execution()
#
# When switching back to TensorFlow 2.x above command should be removed, since
# in TensorFlow 2.x eager execution is enabled by default.

if __name__ == '__main__':

    print('\nRunning demo for the "20 Newsgroups" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '../_data/20newsgroups_text_label_df.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    data_source = dq0.sdk.data.text.CSV(filepath)

    # create model
    model = UserModel()

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
