# -*- coding: utf-8 -*-
"""Utils for data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

from dq0.sdk.estimators.data_handler.csv import CSVDataHandler

data_handler_types = {

    'csv': CSVDataHandler
}


def data_handler_factory(data_handler_instance):
    data_handler_class = data_handler_types[data_handler_instance.lower()]
    return data_handler_class()