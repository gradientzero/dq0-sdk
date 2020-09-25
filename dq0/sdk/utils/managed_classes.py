# -*- coding: utf-8 -*-
"""Managed classes of custom_objects, Optimizers and Losses

Copyright 2020, Gradient Zero
All rights reserved
"""
import tensorflow.compat.v1

import tensorflow_hub as hub

custom_objects = {
    'KerasLayer': hub.KerasLayer,
}

optimizers = {
    'Adagrad': tensorflow.keras.optimizers.Adagrad,
    'Adam': tensorflow.keras.optimizers.Adam,
    'SGD': tensorflow.keras.optimizers.SGD
}

losses = {
    'BinaryCrossentropy': tensorflow.keras.losses.BinaryCrossentropy,
    'CategoricalCrossentropy': tensorflow.keras.losses.CategoricalCrossentropy,
    'CategoricalHinge': tensorflow.keras.losses.CategoricalHinge,
    'CosineSimilarity': tensorflow.keras.losses.CosineSimilarity,
    'Hinge': tensorflow.keras.losses.Hinge,
    'Huber': tensorflow.keras.losses.Huber,
    'KLDivergence': tensorflow.keras.losses.KLDivergence,
    'LogCosh': tensorflow.keras.losses.LogCosh,
    'MeanAbsoluteError': tensorflow.keras.losses.MeanAbsoluteError,
    'MeanAbsolutePercentageError': tensorflow.keras.losses.MeanAbsolutePercentageError,
    'MeanSquaredError': tensorflow.keras.losses.MeanSquaredError,
    'MeanSquaredLogarithmicError': tensorflow.keras.losses.MeanSquaredLogarithmicError,
    'Poisson': tensorflow.keras.losses.Poisson,
    # 'Reduction': tensorflow.keras.losses.Reduction,
    'SparseCategoricalCrossentropy': tensorflow.keras.losses.SparseCategoricalCrossentropy,
    'SquaredHinge': tensorflow.keras.losses.SquaredHinge,
}
