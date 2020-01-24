# -*- coding: utf-8 -*-
"""DQ0 Data Connector class

The connector class serves as the main data connection manager.
It provides methods to list available data sources and reads them via
their specific data source implementaions.

Attributes:
    sources (list): List of available data sources.

Example:
    connector = dq0sdk.data.Connector()
    sources = connector.list()
    data = sources[0].read()

Todo:
    * Implement _detect_sources()

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""
import logging
import os

from .csv import CSVSource

logger = logging.getLogger()


class Connector():
    """Data connector. Manages all data sources available through the SDK.

    Args:
        dataconfig: Data source configuration in yaml format.
    """
    def __init__(self, dataconfig=None):
        super().__init__()
        self.sources = None
        self.dataconfig = dataconfig

    def list(self, reload=False):
        """List available data sources

        Args:
            reload (bool): True to rescan for data sources first

        Returns:
            List of available data sources
        """
        if reload or self.sources is None:
            self._detect_sources()
        return self.sources

    def _detect_sources(self):
        """Scan for available data sources.
        """
        logger.debug('Scanning for new data sources.')
        self.sources = []

        if self.dataconfig is None:
            logger.debug('Data configuration not found!')
            return

        read_allowed_globally = 'read' in self.dataconfig['settings']['allowed_actions']
        meta_allowed_globally = 'meta' in self.dataconfig['settings']['allowed_actions']
        types_allowed_globally = 'types' in self.dataconfig['settings']['allowed_actions']
        stats_allowed_globally = 'stats' in self.dataconfig['settings']['allowed_actions']
        sample_allowed_globally = 'sample' in self.dataconfig['settings']['allowed_actions']

        for source in self.dataconfig['sources']:
            read_allowed = read_allowed_globally
            meta_allowed = meta_allowed_globally
            types_allowed = types_allowed_globally
            stats_allowed = stats_allowed_globally
            sample_allowed = sample_allowed_globally
            if 'settings' in source and 'allowed_actions' in source['settings']:
                read_allowed = 'read' in source['settings']['allowed_actions']
                meta_allowed = 'read' in source['settings']['allowed_actions']
                types_allowed = 'read' in source['settings']['allowed_actions']
                stats_allowed = 'read' in source['settings']['allowed_actions']
                sample_allowed = 'read' in source['settings']['allowed_actions']

            if source['type'] == 'csv':
                csv = CSVSource(source['name'], os.path.join(self.dataconfig['settings']['csv_base_dir'], source['path']))
                csv.read_allowed = read_allowed
                csv.meta_allowed = meta_allowed
                csv.types_allowed = types_allowed
                csv.stats_allowed = stats_allowed
                csv.sample_allowed = sample_allowed
                self.sources.append(csv)

        logger.debug('Found {} available sources'.format(len(self.sources)))
