# -*- coding: utf-8 -*-
"""DQ0 SDK User Data Sources package.

This package contains templates for user defined data sources.
"""

test_case = 'Cifar10'  #  'Newsgroup'

if test_case.lower() == 'Cifar10'.lower():
    from .user_source import UserSource
elif test_case.lower() == 'Newsgroup'.lower():
    from .user_source_newsgroup import UserSource

__all__ = [
    'UserSource'
]
