# -*- coding: utf-8 -*-
"""Data Source for ElasticSearch clients.

This source class provides access to data from an ElasticSearch instance and exposes it as pandas data frames.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source

try:
    from elasticsearch import Elasticsearch
    elastic_search_available = True
except ImportError:
    elastic_search_available = False

import pandas as pd
from pandas.io.json import json_normalize


class ElasticSearch(Source):
    """Data Source for ElasticSearch data.

    Provides function to read data from ElasticSearch.

    ElasticSearch connection string: 'https://[username]:[password]@[host]:[port]/'

    Usage:
        from dq0.sdk.data.clients.elastic_search import ElasticSearch
        es = ElasticSearch(username='elastic', password='password')
        df = es.search(index='my_index', query={"match_all":{}})

    Args:
        protocol (:obj:`str`): Protocol of the ElasticSearch instance (default: 'https')
        host (:obj:`str`): Host of the ElasticSearch instance (default: 'localhost')
        username (:obj:`str`): Username used to connect to the ElasticSearch instance
        password (:obj:`str`): Password used to connect to the ElasticSearch instance
        port (:obj:`int`): Port of the running ElasticSearch instance (default: 9200)
    """

    def __init__(
        self,
        protocol='https',
        host='localhost',
        username='',
        password='',
        port=9200,
        **kwargs
    ):

        password_sep = ':' if 0 < len(password) else ''
        user_sep = '@' if 0 < len(username) else ''
        port_sep = ':' if port is not None else ''
        connection_string = f"{protocol}://{username}{password_sep}{password}{user_sep}{host}{port_sep}{port}/"
        self.connection_string = connection_string
        super().__init__(connection_string, **kwargs)
        self.type = 'elasticsearch'

        # Construct a Elasticsearch client object.
        if not elastic_search_available:
            raise ImportError('elasticsearch dependencies must be installed first')

        self.client = Elasticsearch(
            hosts=self.connection_string,
            **kwargs
        )

        # ping instance
        if self.client.ping() is not True:
            # use self.client.info() ?
            print(self.client.info())
            raise ImportError('elasticsearch ping failed')

    def search(self, index=None, query=None, **kwargs):
        """Search ElasticSearch using index and query

        Args:
            index: Index
            query: Query

        Returns:
            ElasticSearch search result as pandas dataframe
        """
        # checks
        if index is None:
            raise ValueError('you need to pass a index parameter')
        if query is None:
            raise ValueError('you need to pass a query parameter')

        # make an API request
        resp = self.client.search(index=index, query=query, **kwargs)

        # sample result format:
        '''
        {
            "took" : 28,
            "timed_out" : false,
            "_shards" : {
                "total" : 5,
                "successful" : 5,
                "skipped" : 0,
                "failed" : 0
            },
            "hits" : {
                "total" : 1,
                "max_score" : 0.8630463,
                "hits" : [
                {
                    "_index" : "logs",
                    "_type" : "my_app",
                    "_id" : "ZsWdJ2EBir6MIbMWSMyF",
                    "_score" : 0.8630463,
                    "_source" : {
                        "timestamp" : "2018-01-24 12:34:56",
                        "message" : "User logged in",
                        "user_id" : 4,
                        "admin" : false
                    }
                }
                ]
            }
        }
        '''
        # results are stored in _source inside hits.hits
        df = None
        if 'hits' in resp:
            if 'hits' in resp['hits']:
                df = json_normalize(resp['hits']['hits'])

        # return pandas dataframe
        return df

    def read(self, **kwargs):
        """Read json data sources

        Args:
            kwargs: keyword arguments

        Returns:
            json data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        return pd.read_json(self.path, **kwargs)
