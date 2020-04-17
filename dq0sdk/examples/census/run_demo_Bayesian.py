# -*- coding: utf-8 -*-
"""Adult dataset example.
Run script to test the exeuction locally.
Copyright 2019, Gradient Zero
All rights reserved
"""

import os

# from dq0sdk.examples.census.preprocessed.data.user_source import UserSource
# from dq0sdk.examples.census.preprocessed.model.user_model import UserModel

from dq0sdk.examples.census.data.user_source_for_bayesian_model import UserSource
from dq0sdk.examples.census.model.bayesian_user_model import UserModel

from sklearn import model_selection


if __name__ == '__main__':
    # path = 'data/data/adult_with_rand_names.csv'
    # path = 'data/adult_with_rand_names.csv'
    #filepath = os.path.join(os.path.dirname(
    #    os.path.abspath(__file__)), path)
    # init data sourcd
    # dc = UserSource(filepath)

    dc = UserSource()

    # create model
    model = UserModel('notebooks/saved_model/')

    # attach data source
    model.attach_data_source(dc)

    # prepare data
    model.setup_data()

    # setup model
    model.setup_model()


    # model_selection.train_test_split: output type is the same as the
    # input type
    model.X_train, model.X_test, model.y_train, model.y_test = \
        model_selection.train_test_split(
            model.X_train,
            model.y_train,
            test_size=.20,
            shuffle=True,
            stratify=model.y_train)

    # fit the model
    model.fit()

    # evaluate
    acc_tr = model.evaluate(test_data=False)
    acc_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
