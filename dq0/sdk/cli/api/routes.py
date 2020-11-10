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
        '_base': 'projects/',
        'create': '',
        'info': ':uuid/',
        'deploy': ':uuid/deploy/',
        'attach': ':uuid/attach/'
    },
    'model': {
        '_base': 'models/',
        'predict': ':uuid/predict/',
        'register': 'register/'
    },
    'runs': {
        '_base': 'runs/',
        'create': '',
        'get': ':uuid/'
    },
    'job': {
        '_base': 'jobs/:uuid/',
        'state': '',
        'cancel': 'delete/'
    },
    'data': {
        '_base': 'data/',
        'list': '',
        'get': ':uuid/',
        'preprocess': ':uuid/preprocess/',
        'state': ':uuid/state/',
        'info': ':uuid/',
        'sample': ':uuid/sample/',
        'cancel': ':uuid/cancel/'
    }
}


def _build_routes():
    """Helper function to build namespaced routes"""
    r = {}
    for route, subroutes in _routes.items():
        s = {}
        for path, value in subroutes.items():
            if path != '_base':
                s[path] = '{}{}'.format(_routes[route]['_base'], value)
        r[route] = SimpleNamespace(**s)
    return r


routes = SimpleNamespace(**_build_routes())
