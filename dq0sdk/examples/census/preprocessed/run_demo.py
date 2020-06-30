# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the exeuction locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0sdk
from dq0sdk.data.utils import util
from dq0sdk.examples.census.preprocessed.model.user_model import UserModel
from dq0sdk.examples.wrapper_for_sdk_demos import SdkDemo


if __name__ == '__main__':

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state(seed=1)

    # path to input
    path = '../_data/adult_processed.csv'
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
    sdk_demo = SdkDemo(model)
    sdk_demo.fit_model()

    # evaluate the model
    sdk_demo.evaluate_model()
