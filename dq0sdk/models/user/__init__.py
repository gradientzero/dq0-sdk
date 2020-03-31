# -*- coding: utf-8 -*-
"""DQ0 SDK User Model Template project (used by dq0-cli when new project was created).
"""

test_case = 'Cifar10'  # 'Cifar10' 'Newsgroup'

if test_case.lower() == 'Cifar10'.lower():
    from .user_model import UserModel
elif test_case.lower() == 'Newsgroup'.lower():
    from .user_model_newsgroup import UserModel

__all__ = [
    'UserModel'
]
