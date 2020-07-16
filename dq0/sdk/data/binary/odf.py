# -*- coding: utf-8 -*-
"""Data Source for Open Document files.

This source class provides access to Open Document data as pandas dataframes.

This class uses the read function of the ExcelSource class.

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0.sdk.data.binary import Excel


class ODF(Excel):
    """Data Source for Open Document data.

    Provides function to read in Open Document data.

    Args:
        path (:obj:`str`): Absolute path to the Open Document file.
    """
    def __init__(self, path):
        super().__init__(path)
        self.type = 'odf'
