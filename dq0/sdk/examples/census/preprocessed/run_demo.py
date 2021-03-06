# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the exeuction locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0.sdk
from dq0.sdk.data.utils import util
from dq0.sdk.examples.census.preprocessed.model.user_model import UserModel


if __name__ == '__main__':

    print('\nRunning demo for the "Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '../_data/adult_processed.csv'
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
