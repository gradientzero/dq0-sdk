# -*- coding: utf-8 -*-
"""DQ0 SDK User Model Template project (used by dq0-cli when new project was
created).
"""

test_case = 'Patient'  # 'Cifar10' 'Newsgroup' 'Census' Patient

if test_case.lower() == 'Cifar10'.lower():
    from .user_model_cifar10 import UserModel
elif test_case.lower() == 'Newsgroup'.lower():
    from .user_model_newsgroup import UserModel
elif test_case.lower() == 'Census'.lower():
    from .user_model_census import UserModel
elif test_case.lower() == 'Patient'.lower():
    from .user_model_patient import UserModel

__all__ = [
    'UserModel'
]
