# -*- coding: utf-8 -*-
"""Image Data Source.

This is a data source implementation for image data sets.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.data.source import Source

logger = logging.getLogger()


class Image(Source):
    """Data Source for image dataset.

    Attributes:
        folderpath (:obj:`string`): path or url to folder containing the images to load.

    """

    def __init__(self, folderpath):
        super().__init__()
        self.type = 'image'
        self.folderpath = folderpath

    def read(self):
        """Read the image data.

        Returns:
            data (:obj:`pandas.DataFrame`): image data as pd dataframe (no-channels, ch1, ch2, ...)
        """
        return self.folderpath

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        if not self.meta_allowed:
            return {}

        shape = ''
        if self.read_allowed:
            try:
                data = self.read()
                shape = '{}'.format(data.shape)
            except Exception as e:
                logger.debug('Could not get meta info of content. {}'.format(e))

        permissions = []
        if self.read_allowed:
            permissions.append('read')
        if self.meta_allowed:
            permissions.append('meta')
        if self.types_allowed:
            permissions.append('types')
        if self.stats_allowed:
            permissions.append('stats')
        if self.sample_allowed:
            permissions.append('sample')

        return {
            "name": self.name,
            "type": 'image',
            "shape": shape,
            "permissions": permissions
        }
