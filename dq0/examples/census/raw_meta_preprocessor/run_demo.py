# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.examples.census.raw_meta_preprocessor.model.user_model import UserModel
from dq0.sdk.data.metadata.interface.interface import Interface
from dq0.sdk.data.metadata.structure.metadata import Metadata
from dq0.sdk.data.text.csv import CSV
from dq0.sdk.data.utils import util


if __name__ == '__main__':

    print('\nRunning demo for the "Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to metadata
    path = '../_data/adult_with_rand_names_regular_simple.yaml'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    m_interface = Interface(metadata=Metadata.from_yaml_file(filename=filepath))
    data_source = CSV(m_interface.dataset().database())

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
