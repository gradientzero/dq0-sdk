"""diffpriv methods for calculating mean, std and histrograms

calculates differentially private statisitics for
for each column in a pandas dataframe. Used by csv_source.py.

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>
    Craig Lincoln <cl@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""

from diffprivlib import tools as dp

import numpy as np

from sklearn.preprocessing import LabelEncoder


def _min_max(x):
    """Randomizes data column min and max


    The dp methods (mean, std, histrogram) require
    a range input to avoid additional leakage, particularly
    relevant for dp.histrogram as the bins without
    range specified leak the min and max of column.
    Min, max are randomly scaled between 0.9 and 1
    of original values.

    args:
        x (pd.Series): column from dataframe

    returns:
        min, max (tuple): randomized column min, max values
    """
    rand_scale = np.random.ranf(1) * 0.1 + 0.9
    return rand_scale * (np.min(x), np.max(x))


def _dp_mean_std(x, epsilon, randomize_range=True):
    """Calculate dp mean and stdard deviation

    args:
        x (pd.Series): column from dataframe
        epsilon (float): dp privacy percentage (1 = no privacy)
        randomize_range (bool): True to apply randomized max

    returns:
        dp_mean (float): dp column mean
        dp_std (float):  dp column standard deviation
    """
    if randomize_range:
        _range = _min_max(x)[1]
    else:
        _range = None

    dp_mean = dp.mean(x, epsilon, _range)
    dp_std = dp.std(x, epsilon, _range)

    return dp_mean, dp_std


def _get_hist(x, epsilon, randomize_range=True):
    """Calculate column histogram

    args:
        x (pd.Series): column from dataframe
        epsilon (float): dp privacy percentage (1 = no privacy)
        randomize_range (bool): True to apply randomized min, max

    returns:
        hist (np.ndarray): dp counts/bin
        bins (np.ndarray): dp bins
    """
    if randomize_range:
        _range = _min_max(x)
    else:
        _range = None

    hist, bins = dp.histogram(x, epsilon, range=_range)
    hist = hist / hist.sum()

    return hist, bins


def _dp_stats(content, epsilon=1, randomize_range=True):
    """Traverse datafrme columns to return dp stats


    dp_mean and dp_std take only int64 and float64, while
    dp_hist is parsed all pandas data types.

    args:
        content (pd.DataFrame): the data
        epsilon (float): dp privacy percentage (1 = no privacy)
        randomize_range (bool): if True applies randomized max

    returns:
        dp_mean (tuple): dp mean/column
        dp_std (tuple):  dp standard deviation/column
        dp_hist(list): tuple(counts, bins)/column
    """
    dp_mean, dp_std = zip(*[_dp_mean_std(content[col], epsilon, randomize_range) if
                            content[col].dtype in ('int64', 'float64') else
                            tuple([np.nan] * 2) for col in content])

    dp_hist = [_get_hist(content[col], epsilon, randomize_range) if
               content[col].dtype in ('int64', 'float64') else
               _get_hist(LabelEncoder().fit_transform(content[col]), epsilon, randomize_range=False)
               for col in content]
    return dp_mean, dp_std, dp_hist
