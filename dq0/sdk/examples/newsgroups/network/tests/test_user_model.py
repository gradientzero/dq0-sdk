# -*- coding: utf-8 -*-
"""
Test DQ0 NN example for the 20 Newsgroups dataset.

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
from dq0.sdk.examples.newsgroups.network.model.user_model import UserModel

import numpy as np

import sklearn

# import pytest


def test_nn_and_data_setup():
    """
    Test DQ0 NN example for the 20 Newsgroups dataset.

    """

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

    model.X_train, model.X_test, model.y_train, model.y_test = \
        sklearn.model_selection.train_test_split(
            model.X_train, model.y_train, test_size=0.33,
            stratify=model.y_train
        )

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
