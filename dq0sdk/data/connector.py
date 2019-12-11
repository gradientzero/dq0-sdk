# -*- coding: utf-8 -*-
"""DQ0 Data Connector class

The connector class serves as the main data connection manager.
It provides methods to list available data sources and reads them via
their specific data source implementaions.

Attributes:
    sources (list): List of available data sources.

Example:
    connector = dq0.data.Connector()
    sources = connector.list()
    data = sources[0].read()

Todo:
    * Implement _detect_sources()

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
"""


class Connector():
    """Data connector. Manages all data sources available through the SDK.
    """
    def __init__(self):
        super().__init__()
        self.sources = []
        self._detect_sources()

    def list(self, reload=False):
        """List available data sources

        Args:
            reload (bool): True to rescan for data sources first

        Returns:
            List of available data sources
        """
        if reload:
            self._detect_sources()
        return self.sources

    def _detect_sources(self):
        """Scan for available data sources.
        """
        self.sources = []
