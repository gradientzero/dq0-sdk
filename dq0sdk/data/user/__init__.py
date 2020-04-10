# -*- coding: utf-8 -*-
"""DQ0 SDK User Data Sources package.

This package contains templates for user defined data sources.
"""

test_case = 'Census'  # 'Cifar_10' '20_Newsgroups' 'Census'

if test_case.lower() == 'Cifar_10'.lower():
    from dq0sdk.examples.cifar.data.user_source import UserSource
elif test_case.lower() == '20_Newsgroups'.lower():
    from dq0sdk.examples.newsgroups.data.user_source import UserSource
elif test_case.lower() == 'Census'.lower():
    from dq0sdk.examples.census.data.user_source_for_bayesian_model import UserSource

__all__ = [
    'UserSource'
]
