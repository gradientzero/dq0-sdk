# -*- coding: utf-8 -*-
"""Utils package contains helper functions for the SDK API

Copyright 2020, Gradient Zero
All rights reserved
"""

from uuid import UUID


def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID."""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test
