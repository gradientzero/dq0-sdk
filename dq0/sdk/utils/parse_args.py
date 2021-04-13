# -*- coding: utf-8 -*-
"""

Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

logger = logging.getLogger(__name__)


def parse_value(val):
    try:
        # check if is list and parse list
        if val[0] == '[' and val[-1] == ']':
            val = val.strip('[').strip(']').replace('"', '').replace("'", '').split(',')

            parsed_el = []
            # try to parse every element in list
            for el in val:
                try:
                    parsed_el.append(float(el))
                except ValueError:
                    parsed_el.append(el)
            return parsed_el

        else:
            val = val.replace('"', '').replace("'", '')
            # try to parse the values
            try:
                val = float(val)
            except ValueError:
                pass
            return val
    except Exception:
        return val


def parse_kwargs(kwargs):
    for key in kwargs:
        kwargs[key] = parse_value(kwargs[key])

    return kwargs
