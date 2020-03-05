#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make dataset for predict as npy array for demo
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

    pathout = 'data/X_demo_predict.npy'
    pathout = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), pathout)
    np.save(pathout, model.X_test)
