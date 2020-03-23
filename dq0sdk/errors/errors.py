# -*- coding: utf-8 -*-
"""Custom Exceptions for the DQ0 SDK

Copyright 2020, Gradient Zero
All rights reserved
"""


class DQ0SDKError(Exception):
    """General DQ0 SDK Error."""
    pass


def checkSDKResponse(response):
    """Check an SDK response for error and raise
    a DQ0SDKError if neccessary.

    Args:
        response (dict): SDK response JSON dictionary.
    """
    if response is None:
        return
    if 'error' in response and response['error'] != '':
        raise DQ0SDKError(response['error'])
