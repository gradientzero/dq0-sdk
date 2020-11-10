# -*- coding: utf-8 -*-
"""
Test DQ0 CNN example for the CIFAR-10 dataset.

:Authors:
    Paolo Campigotto <pc@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Jona Boeddinhaus <jb@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""
import os
import pickle

import dq0.sdk
from dq0.sdk.data.utils import util
from dq0.sdk.examples.cifar.model.user_model import UserModel

import numpy as np

import pytest


@pytest.mark.slow
def test_cnn_and_data_setup():
    """
    Test DQ0 CNN example for the CIFAR-10 dataset.

    """

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # path to input
    path = '../../../dq0/sdk/examples/cifar/_data/cifar_dummy.csv'
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
    obs_performance_metrics = {
        'train': model.evaluate(test_data=False),
        'test': model.evaluate()
    }

    # predictions
    obs_pred_labels = model.predict(model.X_test)

    # test
    exp_performance_metrics, exp_pred_labels = set_up_expected()
    check_equality(obs_performance_metrics, obs_pred_labels,
                   exp_performance_metrics, exp_pred_labels)


def set_up_expected():
    """
    Define the expected results for the test.

    Returns:
        Python dictionaries and Numpy nd.arrays with expected results
    """

    # get path to folder of this script and "append" suitable sub-folder
    expected_res_folder = os.path.dirname(os.path.abspath(__file__)) + \
        '/_expected_results/'

    with open(expected_res_folder + 'exp_performance_metrics.pkl', 'rb') as f:
        exp_performance_metrics = pickle.load(f)

    with open(expected_res_folder + 'exp_pred_labels.pkl', 'rb') as f:
        exp_pred_labels = pickle.load(f)

    return exp_performance_metrics, exp_pred_labels


def check_equality(obs_performance_metrics, obs_pred_labels,
                   exp_performance_metrics, exp_pred_labels):
    """
    Test for equality.

    """

    print('\n\nObserved performance:')
    util.pretty_print_dict(obs_performance_metrics)
    print('\n\nExpected performance:')
    util.pretty_print_dict(exp_performance_metrics)

    assert exp_performance_metrics == obs_performance_metrics

    assert np.allclose(obs_pred_labels, exp_pred_labels, equal_nan=True)
