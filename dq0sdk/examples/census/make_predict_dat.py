# -*- coding: utf-8 -*-
"""Create a npy archive to be used as prediction data
for the adult dataset example.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.examples.demo.data.user_source import UserSource
from dq0sdk.examples.demo.model.user_model import UserModel

import numpy as np

if __name__ == '__main__':
    path = 'data/adult_whole_processed.csv'
    filepath = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), path)
    # init data source
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
