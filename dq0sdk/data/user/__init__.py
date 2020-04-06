# -*- coding: utf-8 -*-
"""DQ0 SDK User Data Sources package.

This package contains templates for user defined data sources.
"""

test_case = 'Cifar10'  # 'Cifar10' 'Newsgroup' 'Census'

if test_case.lower() == 'Cifar10'.lower():
    from .user_source_cifar10 import UserSource
elif test_case.lower() == 'Newsgroup'.lower():
    from .user_source_newsgroup import UserSource
elif test_case.lower() == 'Census'.lower():
    from .user_source_census import UserSource

__all__ = [
    'UserSource'
]
