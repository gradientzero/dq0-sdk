# -*- coding: utf-8 -*-
"""Data Source base class for SQL-based data sources.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.source import Source


class SQL(Source):
    """Data Source base class for SQL data.

    Attributes:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): General purpose SQL data source connection string.

    Args:
        query (:obj:`str`): SQL query.
        connection (:obj:`str`): General purpose SQL data source connection string.
    """
    def __init__(self, query, connection):
        super().__init__('')
        self.query = query
        self.connection = connection
        self.engine = None
        self.type = 'sql'

    def to_json(self):  # noqa: C901
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        json = super().to_json()
        json["query"] = self.query

        return json
