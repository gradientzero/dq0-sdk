# -*- coding: utf-8 -*-
"""CIFAR-10 example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""
import os

from dq0.examples.cifar.model.user_model import UserModel
from dq0.sdk.data.metadata.structure.utils.dummy_utils import DummyUtils
from dq0.sdk.data.text.csv import CSV
from dq0.sdk.data.utils import util


if __name__ == '__main__':

    print('\nRunning demo for the "CIFAR-10" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '_data/cifar_dummy.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    data_source = CSV(DummyUtils.dummy_meta_database_for_csv(filepath=filepath))

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
