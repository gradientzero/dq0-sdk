# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the data preprocessing exeuction locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0sdk
from dq0sdk.examples.census.raw.model.user_model import UserModel
from dq0sdk.data.utils import util

if __name__ == '__main__':

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state(seed=1)

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

    # execute preprocessing
    dataset = model.preprocess()

    # save the resulting dataset
    dataset.to_csv('out.csv')
