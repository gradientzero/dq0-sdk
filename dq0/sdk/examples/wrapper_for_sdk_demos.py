# -*- coding: utf-8 -*-
"""SDK Runtime helper

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.runtime.runtime import Runtime
from dq0.sdk.data.utils import util


class SdkDemo:
    """
    Wrapper for DQ0-core trainer, to keep it transparent to SDK users.
    """

    def __init__(self, user_model):

        # setup model trainer
        self.trainer = Runtime._get_trainer_for_model(user_model, True)

        if hasattr(user_model, 'metrics'):
            # user_model is a Tensorflow model
            self.model_metrics = user_model.metrics
        else:
            # user_model is a Scikit model
            self.model_metrics = None

    def fit_model(self):
        self.trainer.fit()

    def evaluate_model(self):
        # print('\nModel performance:')
        res_te = self.trainer.evaluate()
        util.print_evaluation_res(res_te, 'test', self.model_metrics)

        res_tr = self.trainer.evaluate(test_data=False)
        util.print_evaluation_res(res_tr, 'training', self.model_metrics)


if __name__ == '__main__':
    #
    # Example of SdkDemo class usage
    #

    import os

    import dq0.sdk
    from dq0.sdk.examples.census.raw.model.user_model import UserModel

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state(seed=1)

    # path to input
    path = './census/_data/adult_with_rand_names.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)

    # init input data source
    data_source = dq0.sdk.data.text.CSV(filepath)

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
