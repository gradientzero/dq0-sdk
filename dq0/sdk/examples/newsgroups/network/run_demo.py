# -*- coding: utf-8 -*-
"""20 Newsgroups dataset example.

Run script to test the execution locally.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.newsgroups import Newsgroups
from dq0.sdk.data.utils import util
from dq0.sdk.examples.newsgroups.network.model.user_model import UserModel

import sklearn

if __name__ == '__main__':

    print('\nRunning demo for the "20 Newsgroups" dataset\n')

    # set seed of random number generator to ensure reproducibility of results
    util.initialize_rnd_numbers_generators_state()

    # init input data source
    data_source = Newsgroups()

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
    model.evaluate()
    model.evaluate(test_data=False)

    print('\nDemo run successfully!\n')
