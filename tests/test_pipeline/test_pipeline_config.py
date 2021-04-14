# -*- coding: utf-8 -*-
"""
Copyright 2021, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.pipeline import transformer # noqa 
from dq0.sdk.pipeline.pipeline_config import PipelineConfig # noqa
from dq0.sdk.pipeline import pipeline # noqa
import numpy as np # noqa
import os # noqa

logger = logging.getLogger(__name__)


def get_data_int():
    X = np.ones((4, 3))
    y_int = np.array([1, 2, 3, 4])

    return X, y_int


def test_pipeline_config_read_001():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pp_config = PipelineConfig(config_path=os.path.join(dir_path, 'pipeline_config.yaml'))
    steps = pp_config.get_steps_from_config()

    pipe = pipeline.Pipeline(steps=steps)

    X, y = get_data_int()
    X_t = pipe.fit_transform(X)
    print(X_t)
    assert X_t[0, 0] == 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_pipeline_config_read_001()