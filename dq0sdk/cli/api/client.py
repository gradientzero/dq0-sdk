# -*- coding: utf-8 -*-
"""Client communicates with the DQ0 CLI API via requests http calls

Client uses the requests library to perform HTTP requests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import requests


class Client:
    """A simple HTTP client

    This class is used to communicate with the DQ0 CLI API.
    It shall not be used directly, but rather is called by Experiment,
    Model and Runner to commit actions and retrieve information via the
    DQ0 CLI API.

    Example:
        # Create an instance
        client = Client()

        # make a request
        route = 'project'
        json_response = client.request(route)

    Args:
        host (str): The host of the DQ0 CLI API Server
        port (int): The port of the DQ0 CLI API Server
    """
    def __init__(self, host='localhost', port=9000):
        self.api = 'http://localhost:9000/api/'
        self.set_connection(host, port)

    def set_connection(self, host='localhost', port=9000):
        """Updates the connection string for the API communication.

        Args:
            host (str): The host of the DQ0 CLI API Server
            port (int): The port of the DQ0 CLI API Server
        """
        if not isinstance(host, str):
            raise ValueError('Wrong host argument')
        if not isinstance(port, int):
            raise ValueError('Wrong port argument')

        try:
            host.index('http')
        except ValueError:
            host = 'http://{}'.format(host)

        self.api = '{}:{}/api/'.format(host, port)
        print('New connection string: {}'.format(self.api))

    def get(self, route, id=None, data=None):
        """Make an HTTP GET request.

        Calles the DQ0 CLI API with a GET request on the given route.

        Returns the response as JSON.
        Throws an error on failure.

        Args:
            route (str): The API route to request.
            id (str): If set this value will replace route's ':id' placeholder
            data (optional, dict): GET data to pass.
        """
        if id is not None:
            route = route.replace(':id', id)
        response = requests.get('{}{}'.format(self.api, route), data=data)
        return response.json()

    def post(self, route, id=None, data=None):
        """Make an HTTP POST request.

        Calles the DQ0 CLI API with a POST request on the given route.

        Returns the response as JSON.
        Throws an error on failure.

        Args:
            route (str): The API route to request.
            id (str): If set this value will replace route's ':id' placeholder
            data (optional, dict): POST data to pass.
        """
        if id is not None:
            route = route.replace(':id', id)
        response = requests.post('{}{}'.format(self.api, route), data=data)
        return response.json()
