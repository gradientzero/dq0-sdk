# -*- coding: utf-8 -*-
"""DQ0 SDK User Model Template project (used by dq0-cli when new project was
created).
"""


import importlib
test_case = 'Patient'  # 'Cifar10' 'Newsgroup' 'Census' Patient

UserModel = None
if test_case.lower() == 'Cifar_10'.lower():
    UserModel = getattr(importlib.import_module('dq0sdk.examples.cifar.model.user_model'), 'UserModel')
elif test_case.lower() == '20_Newsgroups'.lower():
    UserModel = getattr(importlib.import_module('dq0sdk.examples.newsgroups.model.user_model'), 'UserModel')
elif test_case.lower() == 'Census'.lower():
    from .user_model_census import UserModel
    UserModel = getattr(importlib.import_module('dq0sdk.examples.census.model.bayesian_user_model'), 'UserModel')
elif test_case.lower() == 'Patient'.lower():
    from .user_model_patient import UserModel
    

# from .user_model import UserModel

__all__ = [
    'UserModel'
]
