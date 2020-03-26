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
        'info': ':id/',
        'deploy': ':id/deploy/'
    },
    'model': {
        '_base': 'models/:id/',
        'train': 'train/',
        'predict': 'predict/',
        'state': '',
        'cancel': 'cancel/'
    },
    'data': {
        '_base': 'data/',
        'list': '',
        'preprocess': ':id/preprocess/',
        'attach': ':id/attach/',
        'state': ':id/',
        'cancel': 'cancel/'
    }
}


def build_routes():
    r = {}
    for route, subroutes in _routes.items():
        s = {}
        for path, value in subroutes.items():
            if path != '_base':
                s[path] = '{}{}'.format(_routes[route]['_base'], value)
        r[route] = SimpleNamespace(**s)
    return r


routes = SimpleNamespace(**build_routes())
