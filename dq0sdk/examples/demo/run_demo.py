#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make predict set as npy array for demo
"""

import os

from dq0sdk.examples.demo.data.user_source import UserSource
from dq0sdk.examples.demo.model.user_model import UserModel

import numpy as np

if __name__ == '__main__':
    path = 'data/adult_whole_processed.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)
    # init data sourcd
    dc = UserSource(filepath)

    # create model
    model = UserModel('notebooks/saved_model/')

    # attach data source
    model.attach_data_source(dc)

    # prepare data
    model.setup_data()
    
    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate
    loss_tr, acc_tr, mse_te = model.evaluate(test_data=False)
    loss_te, acc_te, mse_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
