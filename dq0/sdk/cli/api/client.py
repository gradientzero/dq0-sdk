# -*- coding: utf-8 -*-
"""Client communicates with the DQ0 CLI API via requests http calls

Client uses the requests library to perform HTTP requests.

Copyright 2020, Gradient Zero
All rights reserved
"""

import json

import requests


class Client:
    """A simple HTTP client

    This class is used to communicate with the DQ0 CLI API.
    It shall not be used directly, but rather is called by Experiment,
    Model and Runner to commit actions and retrieve information via the
    DQ0 CLI API.

    Example:
        >>> # Create an instance
        >>> client = Client() # doctest: +SKIP
        >>>
        >>> # make a request
        >>> route = 'project' # doctest: +SKIP
        >>> json_response = client.request(route) # doctest: +SKIP

    Args:
        host (:obj:`str`): The host of the DQ0 CLI API Server
            (default 'localhost')
        port (int): The port of the DQ0 CLI API Server (default 9000)

    Attributes:
        api (:obj:`str`): The complete API URL, host + port
    """

    def __init__(self, host='localhost', port=9000):
        self.api = 'http://localhost:9000/api/'
        self.set_connection(host, port, False)

    def set_connection(self, host='localhost', port=9000, verbose=True):
        """Updates the connection string for the API communication.

        Args:
            host (:obj:`str`): The host of the DQ0 CLI API Server
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

        if verbose:
            print('New connection string: {}'.format(self.api))

    def get(self, route, uuid=None, data=None):
        """Make an HTTP GET request.

        Calles the DQ0 CLI API with a GET request on the given route.

        Returns the response as JSON.
        Throws an error on failure.

        Args:
            route (:obj:`str`): The API route to request.
            uuid (:obj:`str`): If set this value will replace route's ':uuid' placeholder
            data (optional, dict): GET data to pass.

        Returns:
            The HTTP response in JSON format
        """
        if uuid is not None:
            route = route.replace(':uuid', uuid)
        response = requests.get('{}{}'.format(self.api, route), data=data)
        response_json = self._parse_response(response)
        return response_json

    def post(self, route, uuid=None, data=None):
        """Make an HTTP POST request.

        Calles the DQ0 CLI API with a POST request on the given route.

        Returns the response as JSON.
        Throws an error on failure.

        Args:
            route (:obj:`str`): The API route to request.
            uuid (:obj:`str`): If set this value will replace route's ':uuid' placeholder
            data (:obj:`dict`, optional): POST data to pass.

        Returns:
            The HTTP response in JSON format
        """
        if uuid is not None:
            route = route.replace(':uuid', uuid)
        header = {"content-type": "application/json"}
        response = requests.post('{}{}'.format(self.api, route), data=json.dumps(data), headers=header)
        response_json = self._parse_response(response)
        return response_json

    def _parse_response(self, response):
        """Decodes the response to JSON.

        Args:
            response: The response to parse.

        Returns:
            Parsed JSON response
        """
        response_json = {}
        try:
            response_json = response.json()
        except json.JSONDecodeError as error:
            response_json['error'] = '{}. {}'.format(response, error)
        return response_json
