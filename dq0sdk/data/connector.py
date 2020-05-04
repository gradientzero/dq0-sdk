# -*- coding: utf-8 -*-
"""DQ0 Data Connector class

The connector class serves as the main data connection manager.
It provides methods to list available data sources and reads them via
their specific data source implementations.

Example:
    >>> connector = dq0sdk.data.Connector() # doctest: +SKIP
    >>> sources = connector.list() # doctest: +SKIP
    >>> data = sources[0].read() # doctest: +SKIP

Copyright 2020, Gradient Zero
All rights reserved
"""
import logging
import os

from .csv import CSVSource

logger = logging.getLogger()


class Connector():
    """Data connector. Manages all data sources available through the SDK.

    Args:
        dataconfig (:obj:`dict`): Dictonary of data configuration from YAML.
        working_dir (:obj:`str`, optional): Current working directory.

    Attributes:
        sources (:obj:`list`): List of available data sources.
        dataconfig (:obj:`dict`): Dictonary of data configuration.

    """
    def __init__(self, dataconfig=None, working_dir=None):
        super().__init__()
        self.sources = None
        self.dataconfig = dataconfig
        self.working_dir = working_dir if working_dir is not None else ''

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
            name = source['name']
            description = source['description'] if 'description' in source else ''
            read_allowed = read_allowed_globally
            meta_allowed = meta_allowed_globally
            types_allowed = types_allowed_globally
            stats_allowed = stats_allowed_globally
            sample_allowed = sample_allowed_globally
            if 'settings' in source and 'allowed_actions' in source['settings']:
                read_allowed = 'read' in source['settings']['allowed_actions']
                meta_allowed = 'meta' in source['settings']['allowed_actions']
                types_allowed = 'types' in source['settings']['allowed_actions']
                stats_allowed = 'stats' in source['settings']['allowed_actions']
                sample_allowed = 'sample' in source['settings']['allowed_actions']

            types = []
            if types_allowed:
                types = source['types']

            if source['type'] == 'csv':
                filepath = os.path.join(self.working_dir, self.dataconfig['settings']['csv_base_dir'], source['path'])
                samplepath = None
                if 'sample_path' in source:
                    samplepath = os.path.join(self.working_dir, self.dataconfig['settings']['csv_base_dir'], source['sample_path'])
                csv = CSVSource(filepath)
                csv.name = name
                csv.description = description
                csv.sample_filepath = samplepath
                csv.read_allowed = read_allowed
                csv.meta_allowed = meta_allowed
                csv.types_allowed = types_allowed
                csv.stats_allowed = stats_allowed
                csv.sample_allowed = sample_allowed
                csv.types = types
                self.sources.append(csv)

        logger.debug('Found {} available sources'.format(len(self.sources)))
