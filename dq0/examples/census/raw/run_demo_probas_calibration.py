# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0.examples.census.raw.model.user_model import UserModel
from dq0.makedp.trainer.tf.probability_calibration. \
    neural_network_probs_calibration import CalibratedNeuralNetworkClassifier
from dq0.sdk.data.metadata.structure.utils.dummy_utils import DummyUtils
from dq0.sdk.data.text.csv import CSV
from dq0.sdk.data.utils import util


# TODO this should not stay in the SDK since it imports from dq0.makedp!

if __name__ == '__main__':

    print('\nRunning a demo showing how to learn a calibrated NN for the '
          '"Census" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state(seed=1)

    # path to input
    path = '../_data/adult_with_rand_names.csv'
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

    calibrated_model = CalibratedNeuralNetworkClassifier(model)
    # fit the model and the calibrator
    calibrated_model.fit()

    calibrated_probs = calibrated_model.predict_proba(model.X_test)

    # evaluate the calibrated model
    calibrated_model.evaluate()
    calibrated_model.evaluate(test_data=False)
    calibrated_model.evaluate_probas_calibration(
        output_folder='./output/calibration_demo/'
    )

    print('\nDemo run successfully!\n')
