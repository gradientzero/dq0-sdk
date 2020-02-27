"""Managed classes of custom_objects, Optimizers and Losses

Needed to:
    - instantiate these classes in NeuralNetworkYaml
    - substitute non-dp optimizer for dp version in core

WARNING: for continuous integration this file should be copied
from core to the sdk after any edits.

TODO: check how the none Gaussian optimizers work.
For now we just stick to Gaussian versions.
"""
import tensorflow

import tensorflow_hub as hub

import tensorflow_privacy

custom_objects = {
    'KerasLayer': hub.KerasLayer,
}

optimizers = {
    'Adagrad': tensorflow.keras.optimizers.Adagrad,
    'Adam': tensorflow.keras.optimizers.Adam,
    'SGD': tensorflow.keras.optimizers.SGD,
    # 'DPAdagradOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPAdagradOptimizer,  # to be checked how they work
    # 'DPAdamOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPAdamOptimizer,
    # 'DPGradientDescentOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPGradientDescentOptimizer,
    'DPAdagradGaussianOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPAdagradGaussianOptimizer,
    'DPAdamGaussianOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPAdamGaussianOptimizer,
    'DPGradientDescentGaussianOptimizer': tensorflow_privacy.privacy.optimizers.dp_optimizer.DPGradientDescentGaussianOptimizer,
}

dp_optimizer_alias = {
    'Adagrad': 'DPAdagradGaussianOptimizer',
    'Adam': 'DPAdamGaussianOptimizer',
    'SGD': 'DPGradientDescentGaussianOptimizer',
    'DPAdagradGaussianOptimizer': 'DPAdagradGaussianOptimizer',
    'DPAdamGaussianOptimizer': 'DPAdamGaussianOptimizer',
    'DPGradientDescentGaussianOptimizer': 'DPGradientDescentGaussianOptimizer',
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
    'Reduction': tensorflow.keras.losses.Reduction,
    'SparseCategoricalCrossentropy': tensorflow.keras.losses.SparseCategoricalCrossentropy,
    'SquaredHinge': tensorflow.keras.losses.SquaredHinge,
}
