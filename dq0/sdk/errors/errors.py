# -*- coding: utf-8 -*-
"""Error handling module

Guidelines for handling errors occurring in SDK and plugins
Please use:

logger.warning(), for harmless warning messages. Program execution should not
                  be stopped;

logger.error(),  for an error that DQ0 can recover from. E.g., log an error for
                 a parameter that has been assigned an infeasible value,
                 assign a default feasible value to the parameter and
                 continue program execution;

 dq0.sdk.errors.errors..fatal_error(error_msg)  for an error that DQ0 cannot recover
                from. Program execution is stopped.
                Therefore, to handle fatal exception / error:
                    dq0.sdk.errors.errors.fatal_error(message)
                should be preferred to:
                    logger.fatal(message)
                    return 1.  / sys.exit(1)
Optionally, fatal_error() accepts as input a logger instance and a log-key value.
See below for details.

Copyright 2021, Gradient Zero
All rights reserved
"""


import logging
import sys


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


def fatal_error(error_msg, logger=None):
    """
    Handle fatal errors.

    Args:
        error_msg: string with error message
        logger: Logger instance
    """

    if logger is None:
        logger = logging.getLogger(__name__)

    logger.fatal(error_msg)

    sys.exit(1)
