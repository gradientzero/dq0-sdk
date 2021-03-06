# -*- coding: utf-8 -*-
"""General data utility functions.

Copyright 2020, Gradient Zero
All rights reserved
"""

import inspect
import os
import pickle
import random
import shutil
import sys

import numpy as np

import pandas as pd

import scipy as sp

import tensorflow as tf

import yaml


def load_params_from_config_file(yaml_file_path):
    """
    Load parameters from YAML configuration file.

    Args:
        file_path (:obj:`str`): path to file. Defaults to `config.yml`

    Raises:
        FileNotFoundError: yaml config file not found

    Returns:
        parameters loaded from yaml file
    """
    if not os.path.exists(yaml_file_path):
        raise FileNotFoundError

    with open(yaml_file_path, 'r') as f:
        params_dict = yaml.load(f, Loader=yaml.FullLoader)

        # print(params_dict)

        section_params_dict = params_dict['demo parameters']
        seed = section_params_dict['seed']

        section_params_dict = params_dict['target-model parameters']
        target_model_type = section_params_dict['target_model_type']

        section_params_dict = params_dict['robustness-test parameters']
        precision_threshold = section_params_dict['precision_threshold']
        recall_threshold = section_params_dict['recall_threshold']
        stop_at_first_privacy_breach = section_params_dict[
            'stop_at_first_privacy_breach']

        # print(type(stop_at_first_privacy_breach))
        # print(type(precision_threshold))
        # print(type(recall_threshold))
        # print(type(seed))
        # print(type(target_model_type))

        section_params_dict = params_dict['Differential-privacy parameters']
        dp_epsilons_list = section_params_dict['epsilons']

    return seed, target_model_type, precision_threshold, recall_threshold,  \
        stop_at_first_privacy_breach, dp_epsilons_list


def print_dataset_info(df_dataset, s_title):
    """Print some info about the given dataset.

    Args:
        df_dataset: data frame to print.
        s_title: Title for print output.
    """
    print("\n" + s_title + ". Technical info (RAM usage, etc.): ")
    df_dataset.info(memory_usage='deep')

    nr, nc = df_dataset.shape
    print("\n" + s_title + ": ")
    print("\t# of rows:", nr)
    print("\t# of features:", nc)
    if nc < 1e3:
        print_details_about_df_columns(df_dataset)


def print_details_about_df_columns(df_dataset):
    """Print details about columns of dataset.

    Args:
        df_dataset: data frame to inspect.
    """
    if isinstance(df_dataset, pd.DataFrame):
        _print_feats(df_dataset.columns.values.tolist(), "\tfeatures")
        print("\nfeatures type:")
        _print_dataframe_cols_grouped_by_type(df_dataset)

    print("\nSummary stats for numerical features:")
    print(df_dataset.describe(include=None))  # set to None for numeric
    # features only
    if dataframe_has_columns_of_these_types(df_dataset, [np.object,
                                                         'category']):
        print("\nSummary stats for categorical features:")
        print(df_dataset.describe(include=[np.object, 'category']))


def dataframe_has_columns_of_these_types(df, types_list):
    """Returns true if the dataset has the given types.

    Args:
        df: The dataframe to inspect.
        types_list: list of types to check for.

    Returns:
        True if the types are present in the data frame.
    """
    return not df.select_dtypes(include=types_list).empty


def _print_dataframe_cols_grouped_by_type(df_dataset):
    """Print the dataframe columns grouped by type.

    Args:
        df_dataset: The dataset to print.
    """
    grouped_cols_dict = df_dataset.columns.to_series().groupby(
        df_dataset.dtypes).groups
    for key, value in grouped_cols_dict.items():
        print('\t' + str(key) + ':')
        for f in value:
            print('\t\t' + f)


def print_summary_stats(ts, percentiles, s_col):
    """Print stats."""
    print('\n\nStats for', s_col, 'group: ')
    print('num null values:', ts.isnull().sum())
    print(ts.describe(percentiles=percentiles))
    print("\n\n")


def get_categorical_and_quantitative_features_list(dataset, target_feature):
    """
    Define list of categorical and quantitative features of the input dataset.

    Naming convention:
        "categorical" features:	self-explanatory name
        "quantitative" features: continuous, discrete or ordinal values. The
                                 term "quantitative" is preferred to
                                 "numerical" because also category labels
                                 can be numerical values.
        "target" feature: it contains the learning signal (e.g., labels for
                          a classification problem)

    Args:
        dataset: Pandas DataFrame
        target_feature: feature containing the learning signal (e.g.,
            labels for a classification problem)

    Returns:
        Python list of categorical and quantitative features
    """
    column_names_list = dataset.columns

    # get categorical features
    categorical_features_list = [
        col for col in dataset.columns
        if col != target_feature and dataset[col].dtype == 'object']

    # List difference. Warning: in below operation, set does not preserve
    # the order. If order matters, use, e.g., list comprehension.
    quantitative_features_list = \
        list(set(column_names_list) - set(categorical_features_list) - {
            target_feature})

    return categorical_features_list, quantitative_features_list


def sparse_scipy_matrix_to_Pandas_df(sp_matr, sparse_representation=True,
                                     columns_names_list=None):
    """
    Convert Scipy matrix to pandas dataframe.

    Args:
        sp_matr (:obj:`scipy.sparse.spmatrix`): The origin matrix
        sparse_representation (bool): True if the matrix is sparse
        columns_names_list: list of column names

    Returns:
        converted pandas dataframe.
    """
    dense_representation = not sparse_representation
    if sparse_representation:
        df = pd.DataFrame.sparse.from_spmatrix(sp_matr,
                                               columns=columns_names_list)
    elif dense_representation:
        df = pd.DataFrame(sp_matr.todense(), columns=columns_names_list)

    return df


def pretty_print_strings_list(l_strings, s_list_name=None):
    """Print string list."""
    if len(l_strings) > 0:
        if s_list_name is None:
            s_list_name = ''
        _print_feats(l_strings, s_list_name)
    else:
        if s_list_name is not None:
            print('\nNo ' + s_list_name)


def _print_feats(l_column_names, s_title):
    """print column names one per line"""
    print("\n\t".join(([s_title + ': '] + l_column_names)))


def pretty_print_dict(d, indent_steps=1, indent_unit='  '):
    """Print dictionary."""
    for key, value in d.items():
        if isinstance(value, dict):
            print(indent_unit * indent_steps + str(key) + ': ')
            pretty_print_dict(value, indent_steps + 1)
        else:
            print(indent_unit * indent_steps + str(key) + ': ' + str(value))


def pretty_diplay_string_on_terminal(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    column_display_size = 80
    if len(s) <= column_display_size:
        print(s)
    else:
        up_to_char = column_display_size - 3
        print(s[:up_to_char] + '...')


def print_full_df(df_dataset):
    """Print whole dataframe. By default, just reduced output is printed"""

    # to display full contents of dataframe without any kind of truncation:
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    print(df_dataset)

    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.max_colwidth')


def missing_values_table(df):
    """Generate per feature stats about missing values
    to preview the missing values and the % of missing values in each column
    """
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    return mis_val_table_ren_columns


def case_insensitive_str_comparison(string1, string2):
    """Compare strings case insensitive."""
    if isinstance(string2, str):
        if string1.lower() == string2.lower():
            res = True
        else:
            res = False
    elif isinstance(string2, list):
        if string1.lower() in [x.lower() for x in string2]:
            res = True
        else:
            res = False
    return res


def str_to_bool(s):
    """Convert string to bool"""
    if s.lower() in ("yes", "true", "t", "1"):
        return True
    elif s.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError


def string_contains_numeric_value(s):
    """Returns true if the string is convertible to float."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def redirect_stdout_stderr_streams_to_file(log_file):
    """Redirect the stdout and stderr streams to the given log file."""
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    log_file_stream = open(log_file, mode='w')
    sys.stdout = log_file_stream
    sys.stderr = log_file_stream

    return log_file_stream, orig_stdout, orig_stderr


def restore_stdout_stderr_streams(file_stream, orig_stdout, orig_stderr):
    """Restore back stdout and stderr."""
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    file_stream.close()


def get_fn(file_path):
    """Get filename and extension for file path."""
    base = os.path.basename(file_path)
    just_fn, ext = os.path.splitext(base)
    return just_fn, ext


def empty_folder(path_folder_tbr):
    """Empties or creates the given folder."""
    if os.path.exists(path_folder_tbr):
        shutil.rmtree(path_folder_tbr)
    os.makedirs(path_folder_tbr)


def move_files(l_path_files, s_dest_folder):
    """Move files."""
    l_path_new_files = []
    try:
        for s_path_file in l_path_files:
            fn = os.path.basename(s_path_file)
            if not s_dest_folder.endswith('/'):
                s_dest_path_file = s_dest_folder + '/' + fn
            else:
                s_dest_path_file = s_dest_folder + fn
            if os.path.isfile(s_dest_path_file):
                os.remove(s_dest_path_file)
            os.rename(s_path_file, s_dest_path_file)
            l_path_new_files.append(s_dest_path_file)

        return l_path_new_files

    except Exception as e:
        sys.exit('\n\nCannot move file ' + s_path_file + ' into '
                 'folder ' + s_dest_folder + '! ', e)


def list_subfloders(path='./', s_prefix=None):
    """List sub folders.
    Subfolder name starts with given s_prefix ('_starting_with_certain_name_prefix')
    """
    if s_prefix is None:
        l_sf = [d for d in os.listdir(path) if os.path.isdir(d)]
    else:
        l_sf = [d for d in os.listdir(path) if (
                os.path.isdir(d) and d.startswith(s_prefix))]

    return l_sf


def print_human_readable_elapsed_time_value(elapsed_cpu_time_sec, s_tmp):
    """Print elapsed time in human readable format."""
    if elapsed_cpu_time_sec >= (60 * 60 * 24):
        elapsed_cpu_time = round(elapsed_cpu_time_sec / (60 * 60 * 24), 2)
        time_measure = 'day'
    elif elapsed_cpu_time_sec >= (60 * 60):
        elapsed_cpu_time = round(elapsed_cpu_time_sec / (60 * 60), 2)
        time_measure = 'hour'
    elif elapsed_cpu_time_sec >= 60:
        elapsed_cpu_time = round(elapsed_cpu_time_sec / 60.0)
        time_measure = 'minute'
    elif elapsed_cpu_time_sec >= 1:
        elapsed_cpu_time = round(elapsed_cpu_time_sec)
        time_measure = 'sec'
    elif elapsed_cpu_time_sec >= 1e-3:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e3)
        time_measure = 'millisec'
    elif elapsed_cpu_time_sec >= 1e-6:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e6)
        time_measure = 'microsec'
    elif elapsed_cpu_time_sec >= 1e-9:
        elapsed_cpu_time = round(elapsed_cpu_time_sec * 1e9)
        time_measure = 'nanosec'
    else:
        elapsed_cpu_time = elapsed_cpu_time_sec
        time_measure = 'less than one nanosec'

    if elapsed_cpu_time > 1:
        time_measure += 's'

    if time_measure != 'less than one nanosec':
        print(s_tmp + ' {:.2f}'.format(elapsed_cpu_time) + ' ' + time_measure)
    else:
        print(s_tmp + ' ' + time_measure)


def dump_model(model, path='./data/output', name='model.pickle'):
    """Pickle dump given model."""
    with open(os.path.join(path, name), 'wb') as f:
        pickle.dump(model, f)


def load_model_from_file(path):
    """Load model from file."""
    with open(path, 'rb') as file:
        return pickle.load(file)


def get_percentage_freq_of_values(x_np_a):
    """Compute percentage frequencies of values in the input Numpy array

    Args:
        x_np_a (:obj:`numpy.ndarray`): array of values parse

    Returns:
        dictionary with percentage frequencies of values
    """
    vals, counts = np.unique(x_np_a, return_counts=True)
    freqs = ((counts.astype('float32') / sum(counts)) * 100.0)
    return dict(zip(vals, freqs))


def estimate_freq_of_labels(y):
    """Estimate the frequency of labels in y."""
    if isinstance(y, pd.Series):
        print(y.value_counts(normalize=True) * 100)
    else:
        assert isinstance(y, np.ndarray)
        # print(pd.Series(y).value_counts(normalize=True) * 100)

        # print('Label     percentage freq.')
        # pretty_print_dict(get_percentage_freq_of_values(y))

        for key, value in get_percentage_freq_of_values(y).items():
            print('  label "' + str(key) + '": %.1f%%' % value)


def compute_features_bounds(X):
    """
    Compute min / max value for each feature.
    :param X: data matrix (features are the columns).
    :return: ordered list of tuples with min/max values for each feature.
             Order of the list is the order of the columns in the data matrix.
    """

    if isinstance(X, pd.DataFrame):
        min_values = X.min(axis=0).values
        max_values = X.max(axis=0).values
    elif isinstance(X, np.ndarray):
        min_values = X.min(axis=0)
        max_values = X.max(axis=0)

    features_bounds = list(zip(min_values, max_values))
    return features_bounds


def save_preprocessed_tr_and_te_datasets(X_train, X_test, y_train, y_test,
                                         working_folder):
    """Save train and test dataset

    Args:
        X_train: Pandas Dataframe or numpy array
        X_test: Pandas Dataframe or numpy array
        y_train: Pandas Series or numpy (also non-dimensional) array
        y_test: Pandas Series or numpy (also non-dimensional) array
        working_folder: str with file path
    """
    if isinstance(X_train, pd.DataFrame):

        pd.concat([X_train, y_train], axis=1).to_csv(
            working_folder + 'preprocessed_training_data.csv', index=False)
        pd.concat([X_test, y_test], axis=1).to_csv(
            working_folder + 'preprocessed_test_data.csv', index=False)

    elif isinstance(X_train, np.ndarray):

        if y_train.ndim < 2:
            # transform one-dimensional array into column vector via
            # newaxis
            y_train = y_train[:, np.newaxis]
            y_test = y_test[:, np.newaxis]

        if X_train.ndim <= 2:
            np.savetxt(working_folder + 'preprocessed_training_X.csv',
                       X_train, delimiter=',')
            np.savetxt(working_folder + 'preprocessed_test_X.csv',
                       X_test, delimiter=',')
        else:
            np.save(working_folder + 'preprocessed_training_X.npy', X_train)
            np.save(working_folder + 'preprocessed_test_X.npy', X_test)

        np.savetxt(working_folder + 'preprocessed_training_y.csv',
                   y_train, delimiter=',')
        np.savetxt(working_folder + 'preprocessed_test_y.csv',
                   y_test, delimiter=',')


def check_data_structure_type_consistency(X_train, X_test, y_train, y_test):
    """Check for type consistency among train and test X, y.

    Type consistency is achieved iff:
        - all X and y must are Pandas objects
        - all X and y must are Numpy objects
        - y_train, y_test must have the same number of dimensions
    Mixture of Pandas and Numpy objects is not allowed.

    Args:
        X_train: Numpy array or Pandas DataFrame
        X_test: Numpy array or Pandas DataFrame
        y_train: Numpy (also non-dimensional) array or Pandas Series
        y_test: Numpy (also non-dimensional) array or Pandas Series

    """
    assert (isinstance(X_train, pd.DataFrame) or
            isinstance(X_train, np.ndarray))

    assert isinstance(y_train, pd.Series) or isinstance(y_train, np.ndarray)

    if isinstance(X_train, pd.DataFrame):
        if not isinstance(y_train, pd.Series):
            raise Exception('ERROR! Expected y_train type pd.Series, '
                            'but found np.ndarray')

    if isinstance(X_train, np.ndarray):
        if not isinstance(y_train, np.ndarray):
            raise Exception('ERROR! Expected y_train type np.ndarray, '
                            'but found pd.Series')

    if X_test is None:
        assert y_test is None
    else:
        assert y_test is not None
        assert type(X_train) == type(X_test)
        assert type(y_train) == type(y_test)
        if isinstance(y_train, np.ndarray):
            assert y_train.ndim == y_test.ndim


def concatenate_train_test_datasets(X_train, X_test, y_train, y_test):
    """Concetenates train and test datasets

    Args:
        X_train: Numpy array or Pandas DataFrame
        X_test: Numpy array or Pandas DataFrame
        y_train: Numpy (also non-dimensional) array or Pandas Series
        y_test: Numpy (also non-dimensional) array or Pandas Series

    Returns:
        Concatenated X and y
    """
    if isinstance(X_train, pd.DataFrame):
        X, y = concatenate_train_test_datasets_pd_Dataframes(
            X_train, X_test, y_train, y_test
        )
    else:
        if not isinstance(X_train, np.ndarray):
            raise Exception('X_train is neither np.ndarray nor pd.DataFrame')
        X, y = concatenate_train_test_datasets_np_array(
            X_train, X_test, y_train, y_test
        )
    return X, y


def concatenate_train_test_datasets_pd_Dataframes(X_train_df, X_test_df,
                                                  y_train_se, y_test_se):
    """Concatenates train and test datasets

    Args:
        X_train_df: Pandas DataFrame
        X_test_df: Pandas DataFrame
        y_train_se: Pandas Series
        y_test_se: Pandas Series

    Returns:
        Concatenated X and y
    """

    # X: matrix of size (num_examples, num_features)
    # y: vector of class labels
    if X_train_df is not None:
        X_df = X_train_df
        y_se = y_train_se

        if X_test_df is not None:
            X_df = X_train_df.append(X_test_df, ignore_index=True)
            y_se = y_train_se.append(y_test_se, ignore_index=True)
    else:
        # X_test_df is not None
        X_df = X_test_df
        y_se = y_test_se

    return X_df, y_se


def concatenate_train_test_datasets_np_array(X_train_np_a, X_test_np_a,
                                             y_train_np_a, y_test_np_a):
    """Concatenates train and test datasets

    Args:
        X_train_np_a: numpy array
        X_test_np_a: numpy array
        y_train_np_a: numpy (also non-dimensional) array
        y_test_np_a: numpy (also non-dimensional) array

    Returns:
        Concatenated X and y
    """
    if X_test_np_a is None or X_train_np_a is None:
        X_np_a = X_train_np_a if X_test_np_a is None else X_test_np_a
    else:
        X_np_a = np.append(X_train_np_a, X_test_np_a, axis=0)

    if y_train_np_a is not None and y_train_np_a.ndim < 2:
        # transform one-dimensional array into column vector via newaxis
        y_train_np_a = y_train_np_a[:, np.newaxis]
    if y_test_np_a is not None and y_test_np_a.ndim < 2:
        y_test_np_a = y_test_np_a[:, np.newaxis]

    if y_test_np_a is None or y_train_np_a is None:
        y_np_a = y_train_np_a if y_test_np_a is None else y_test_np_a
    else:
        y_np_a = np.append(y_train_np_a, y_test_np_a, axis=0)

    return X_np_a, y_np_a


def numerical_datasets_are_equal(d1, d2, approx_error=1e-4):
    """Compare two numerical datasets for equality. A small tolerance value is
    considered for floating-point error mitigation. I.e., values d1[i,
    j] and d2[i,j] are considered equal iff:
                abs(d1[i,j] - d2[i,j]) < approx_error

    Input Pandas DataFrames / Series (if any) must not contain non-numeric
    values. d1 and d2 types may be different.

        Args:
            d1: Numpy array or Pandas DataFrame or Pandas Series
            d2: Numpy array or Pandas DataFrame or Pandas Series
            approx_error: tolerance value for equality in floating-point arithmetic

    Returns:
        Boolean value True / False if d1 and d2 are / are not equal
    """

    for d in [d1, d2]:
        if not isinstance(d, np.ndarray) and not isinstance(d, pd.DataFrame)\
                and not isinstance(d, pd.Series):
            raise Exception('d type must be np.ndarray, pd.DataFrame or '
                            'pd.Series')

    if isinstance(d1, pd.DataFrame) or isinstance(d1, pd.Series):
        d1 = d1.values

    if isinstance(d2, pd.DataFrame) or isinstance(d2, pd.Series):
        d2 = d2.values

    if d1.shape != d2.shape:
        raise Exception('Comparison for equality of two datasets with '
                        'different shapes: ' + str(d1.shape) + ' and ' + ''
                        '' + str(d2.shape))

    # if isinstance(d1, pd.DataFrame):
    #    return not ((d1 - d2).abs() >= approx_error).any()

    return np.all(np.absolute(d1 - d2) < approx_error)


def datasets_are_equal(d1, d2):
    """Compare two datasets for equality.

        Args:
            d1: Numpy array or Pandas DataFrame or Pandas Series
            d2: Numpy array or Pandas DataFrame or Pandas Series

    Returns:
        Boolean value True / False if d1 and d2 are / are not equal
    """

    for d in [d1, d2]:
        if not isinstance(d, np.ndarray) and not isinstance(d, pd.DataFrame)\
                and not isinstance(d, pd.Series):
            raise Exception('d type must be np.ndarray, pd.DataFrame or '
                            'pd.Series')

    if isinstance(d1, pd.DataFrame):
        if isinstance(d2, pd.DataFrame):
            return d1.equals(d2)
        else:
            raise Exception('Comparing for equality a ' + type(d1) + ''
                            'with a ' + type(d2))

    if isinstance(d1, pd.Series):
        if isinstance(d2, pd.Series):
            return d1.equals(d2)
        else:
            raise Exception('Comparing for equality a ' + type(d1) + ''
                            'with a ' + type(d2))

    if isinstance(d1, np.ndarray):
        if isinstance(d2, np.ndarray):
            if d1.shape != d2.shape:
                raise Exception('Comparing for equality two Numpy arrays '
                                'with different shapes: ' + str(d1.shape) + ''
                                ' and ' + str(d2.shape))
            else:
                return np.allclose(d1, d2)
        else:
            raise Exception('Comparing for equality a ' + type(d1) + ''
                            'with a ' + type(d2))


def initialize_rnd_numbers_generators_state(seed=1, verbose=True):
    """Initialize tf random generator.

    Args:
        seed (int, optional): random seed. Default is 1.
        verbose (bool, optional): Boolean flag to print seed used.
    """
    # get Tensorflow version (first number only)
    tf_version = int(tf.__version__.split('.')[0])

    np.random.seed(seed)

    if tf_version == 1:
        # tf.set_random_seed(seed)  deprecated
        tf.compat.v1.set_random_seed(seed)
    elif tf_version > 1:
        tf.random.set_seed(seed)

    sp.random.seed(seed)
    random.seed(seed)

    if verbose:
        print('\n\nPRNG seeded with value ', seed, '\n')


def manage_rnd_num_generators_state(action):
    """Save and restore the internal states of the random number generators used

    Args:
        action (str): Manage action. Options: 'save'
    """
    if case_insensitive_str_comparison(action, 'save'):
        # workaround to have function-level static variables in Python
        if 'rnd_num_gens_state' not in \
                manage_rnd_num_generators_state.__dict__:
            manage_rnd_num_generators_state.rnd_num_gens_state = \
                {
                    'random': random.getstate(),
                    'numpy': np.random.get_state(),
                    'scipy': sp.random.get_state()
                }
        else:
            raise RuntimeError('rnd numbers generators state already saved!')

    if case_insensitive_str_comparison(action, 'restore'):

        if 'rnd_num_gens_state' in manage_rnd_num_generators_state.__dict__:
            random.setstate(
                manage_rnd_num_generators_state.rnd_num_gens_state['random']
            )
            np.random.set_state(
                manage_rnd_num_generators_state.rnd_num_gens_state['numpy']
            )
            sp.random.set_state(
                manage_rnd_num_generators_state.rnd_num_gens_state['scipy']
            )
        else:
            raise RuntimeError('cannot restore rnd numbers generators state! '
                               'No state previously saved! ')


def print_evaluation_res(res, dataset_type, model_metrics=None):
    """
    Print the results of call of trainer.evaluate()

    Args:
        res (:obj:`dict`): Results returned by trainer.evaluate()
        dataset_type (:obj:`str`): string with two possible values:
        "training" or "test"
        model_metrics (:obj:`list`): list of metrics specified in user model

    """

    if model_metrics is None:
        # user_model is a Scikit model
        for metric in res.keys():
            print('Model ' + metric.replace('_', ' ') + ' on '
                  '' + dataset_type + ' set: %.1f%%' % (100 * res[metric]))

    else:
        # user_model is a Tensorflow model
        if not isinstance(model_metrics, list):
            model_metrics = [model_metrics]

        for metric in model_metrics:
            print('Model ' + metric.replace('_', ' ') + ' on '
                  '' + dataset_type + ' set: %.1f%%' % (
                      100 * res[_fix_metric_names(metric)])
                  )


def _fix_metric_names(metric):
    """
    In Tensorflow there is a mismatch between the metric names that a user can
    specify and the metric names used internally.

    Args:
            metric (:obj:`str`): name given by user

    Returns:
        Metric name used internally by Tensorflow corresponding to the
        metric name specified by the user
    """

    if metric.lower() == 'accuracy':
        metric = 'acc'
    elif metric.lower() == 'mse':
        metric = 'mean_squared_error'

    return metric


def instantiate_metrics_from_name(metrics_list):
    """
    Instantiate a metric class from tensorflow.keras.metrics

    Iterate through metrics_list and replace each string (each string contains
    a metric name) with an instance of the corresponding metric class.

    Args:
        metrics_list: list of metrics defined by user. It may contain
            objects of metric classes or strings with metric names.

    Returns:
        modified metrics_list

    """

    # get every class defined in the tensorflow.keras.metrics module
    keras_metric_classes_l = [m[1] for m in inspect.getmembers(
        tf.keras.metrics, inspect.isclass)]
    # print(keras_metric_classes_l)

    for pos, metric in enumerate(metrics_list):
        if isinstance(metric, str):
            found = False
            for km_class in keras_metric_classes_l:
                if case_insensitive_str_comparison(km_class.__name__, metric):
                    found = True
                    metrics_list[pos] = km_class()
                    break

            if not found:
                raise RuntimeWarning('Metric ' + metric + ' ignored since '
                                     'it is not a valid Keras metric')

    return metrics_list


def compute_metrics_scores(y, y_pred_np_a, metrics_list):
    """
    Iterate through metrics_list and compute each metric in the list. Each
    list item is expected to be an instance of a tensorflow.keras.metrics
    class. So this function call must be preceded by the call to function
    instantiate_metrics_from_name.

    Args:
        y: vector with actual classification labels or regression scores
        y_pred_np_a: vector with predicted classification labels or regression
            scores
        metrics_list: list of instances of metric classes
    Returns:
        dictionary with (metric name, metric score) pairs
    """

    res = {}
    for metric in metrics_list:
        _ = metric.update_state(y, y_pred_np_a)
        # metric_name = metric.name if metric.name is not None \
        #    else metric.__class__.__name__
        metric_name = metric.__class__.__name__.lower()

        # convert tensor to array and update dict
        res.update({metric_name: metric.result().numpy()})
        metric.reset_states()

    return res


def copy_obj_attributes(obj_from, obj_to, attributes_l=None):
    """
    Copy attributes of class instance (object) "obj_from" to class instance
    (object) "obj_to". The two objects are assumed to be instances of the
    same class.

    Args:
        obj_from: class instance (object) to copy from
        obj_to: class instance (object) to copy to
        attributes_l: list of attributes to be copied. If none, a
        blind copy is performed, where all attributes of obj_from are copied
        to obj_to.

    Returns:
        obj_to
    """

    assert isinstance(obj_from, obj_to.__class__)

    if attributes_l is None:
        # blind copy: copy all attributes of obj_from
        obj_to.__dict__.update(obj_from.__dict__)
    else:
        # copy selected attributes only
        for attr in attributes_l:
            if hasattr(obj_from, attr):
                value = getattr(obj_from, attr)
                setattr(obj_to, attr, value)

    return obj_to
