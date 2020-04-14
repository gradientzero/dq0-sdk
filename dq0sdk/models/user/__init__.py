# -*- coding: utf-8 -*-
"""DQ0 SDK User Model Template project (used by dq0-cli when new project was
created).
"""

import importlib


test_case = 'Census'  # 'Cifar_10' '20_Newsgroups' 'Census'

module = None
if test_case.lower() == 'Cifar_10'.lower():
    module = importlib.import_module('dq0sdk.examples.cifar.model.user_model')
elif test_case.lower() == '20_Newsgroups'.lower():
    module = importlib.import_module('dq0sdk.examples.newsgroups.model.user_model')
elif test_case.lower() == 'Census'.lower():
    module = importlib.import_module('dq0sdk.examples.census.model.bayesian_user_model')
from module import UserModel  # noqa: E204

# from .user_model import UserModel

__all__ = [
    'UserModel'
]
