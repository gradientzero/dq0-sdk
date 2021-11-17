# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""
import os

import dq0.sdk
from dq0.examples.medical_insurance.demo_with_preprocessor.model.user_model import UserModel
from dq0.sdk.data.utils import util


if __name__ == '__main__':

    print('\nRunning demo for the "Medical insurance" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '../_data/datasets_13720_18513_insurance.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), *path.split('/'))

    # init input data source
    data_source = dq0.sdk.data.text.CSV(filepath)

    # create model
    model = UserModel()

    # attach data source
    model.attach_data_source(data_source)

    # prepare data
    model.setup_data()
    import numpy as np
    print(np.hstack([model.y_train, model.y_test]))

    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate the model
    model.evaluate()
    model.evaluate(test_data=False)

    print('\nDemo run successfully!\n')
