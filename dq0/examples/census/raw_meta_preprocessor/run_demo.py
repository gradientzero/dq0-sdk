# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

import dq0.sdk
from dq0.examples.census.raw_meta_preprocessor.model.user_model import UserModel
from dq0.sdk.data.metadata.filter.filter_machine_learning import FilterMachineLearning
from dq0.sdk.data.metadata.metadata import Metadata
from dq0.sdk.data.utils import util


if __name__ == '__main__':

    print('\nRunning demo for the "Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to metadata
    path = '../_data/adult_with_rand_names.yaml'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    metadata = Metadata.from_yaml_file(filename=filepath)
    uri = metadata.dataset_node.child_nodes[0].child_nodes[0].child_nodes[0].get_attribute(key='connector').get_attribute(key='uri').value
    meta_ml = metadata.filter(dataset_filter_func=FilterMachineLearning.filter)
    data_source = dq0.sdk.data.text.CSV(uri, meta_ml)

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
