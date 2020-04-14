# -*- coding: utf-8 -*-
"""DQ0 SDK User Data Sources package.

This package contains templates for user defined data sources.
"""

import importlib


test_case = 'Census'  # 'Cifar_10' '20_Newsgroups' 'Census'

module = None
if test_case.lower() == 'Cifar_10'.lower():
    module = importlib.import_module('dq0sdk.examples.cifar.data.user_source')
elif test_case.lower() == '20_Newsgroups'.lower():
    module = importlib.import_module('dq0sdk.examples.newsgroups.data.user_source')
elif test_case.lower() == 'Census'.lower():
    module = importlib.import_module('dq0sdk.examples.census.data.user_source_for_bayesian_model')
from module import UserSource  # noqa: E402

__all__ = [
    'UserSource'
]
