# -*- coding: utf-8 -*-
"""Base data handler.

Copyright 2021, Gradient Zero
All rights reserved
"""

from abc import ABC, abstractmethod
import logging
logger = logging.getLogger(__name__)


class BasicDataHandler(ABC):
    """Basic Data Handler for all estimators"""

    def __init__(self):
        pass

    def setup_data(self, data_source, **kwargs):
        """ Empty setup data, just returns the data source
        """
        return data_source.read()
