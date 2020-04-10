# -*- coding: utf-8 -*-
"""DQ0 SDK User Model Template project (used by dq0-cli when new project was
created).
"""

test_case = 'Census'  # 'Cifar_10' '20_Newsgroups' 'Census'

if test_case.lower() == 'Cifar_10'.lower():
    from dq0sdk.examples.cifar.model.user_model import UserModel
elif test_case.lower() == '20_Newsgroups'.lower():
    from dq0sdk.examples.newsgroups.model.user_model import UserModel
elif test_case.lower() == 'Census'.lower():
    from dq0sdk.examples.census.model.bayesian_user_model import UserModel

# from .user_model import UserModel

__all__ = [
    'UserModel'
]
