# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""
import os

import dq0sdk
from dq0sdk.examples.medical_insurance.model.user_model import UserModel

from dq0.runtime.models.tf.neural_network_trainer_regression import \
    NeuralNetworkTrainerRegression


def print_evaluation_res(res, dataset_type, model_metrics):
    """
    Print the results of call of trainer.evaluate()

    Args:
        res (:obj:`dict`): Results returned by trainer.evaluate()
        dataset_type (:obj:`str`): string with two possible values:
        "training" or "test"
        model_metrics (:obj:`list`): list of metrics specified in user model

    """
    if type(model_metrics) != list:
        model_metrics = [model_metrics]

    for metric in model_metrics:
        print('\t' + metric.replace('_', ' ') + ' on ' + dataset_type
              + ' set: %.2f %%' % (100 * res[metric]))


if __name__ == '__main__':

    # path to input
    path = './_data/datasets_13720_18513_insurance.csv'
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

    # setup model trainer
    disable_DP = False
    if not disable_DP:
        DP_SGD_params_dict = {
            'l2_norm_clip': 1.0,
            'noise_multiplier': 1.1,
            'num_microbatches': 250
        }
    else:
        DP_SGD_params_dict = None

    trainer = NeuralNetworkTrainerRegression(
        model, disable_DP, DP_SGD_params_dict
    )

    # fit the model
    trainer.fit()

    print('\nModel performance:')
    res_tr = trainer.evaluate(test_data=False)
    print_evaluation_res(res_tr, 'training', model.metrics)
    res_te = trainer.evaluate()
    print_evaluation_res(res_te, 'test', model.metrics)
