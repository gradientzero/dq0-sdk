# -*- coding: utf-8 -*-
"""Routes defines all available DQ0 API routes.

Use the a route to select an action and do the request like this:
    client.request(routes.project.info, {'some': 'data'})

Copyright 2020, Gradient Zero
All rights reserved
"""

from types import SimpleNamespace


_routes = {
    'project': {
        'base': 'projects/',
        'info': ''
    },
    'model': {
        'base': 'models/',
        'train': 'train/',
        'predict': 'predict/'
    },
    'data': {
        'base': 'data/',
        'preprocess': 'preprocess/'
    }
}


def build_routes():
    r = {}
    for route, subroutes in _routes.items():
        for path, value in subroutes.items():
            s = {}
            if value != 'base':
                s[path] = '{}{}'.format(_routes[route]['base'], value)
        r[route] = SimpleNamespace(**s)
    return r


routes = SimpleNamespace(**build_routes())
