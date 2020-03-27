# -*- coding: utf-8 -*-
"""Adult dataset example.

Run script to test the exeuction locally.

Example:
    ```bash
    ./dq0 project create --name demo
    cd demo
    copy user_source.py to demo/data/
    copy user_model.py to demo/model/
    ../dq0 data list
    ../dq0 model attach --id <dataset id>
    ../dq0 project deploy
    ../dq0 model train
    ../dq0 model state
    ../dq0 model predict --input-path </path/to/numpy.npy>
    ../dq0 model state
    ```

Copyright 2019, Gradient Zero
All rights reserved
"""

import os

from dq0sdk.examples.demo.data.user_source import UserSource
from dq0sdk.examples.demo.model.user_model import UserModel


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
