# -*- coding: utf-8 -*-
"""User Data Source.

This is a template for user defined data sources.
When training a model on a certain deta source dq0-core is looking for a
UserSource class that is to be used as the custom data source implementation.

This template class derives from Source. Actual implementations should derive
from child classes like CSVSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0sdk.data.csv.csv_source import CSVSource
from dq0sdk.data.preprocessing import preprocessing
from dq0sdk.data.utils import util

import pandas as pd


logger = logging.getLogger()


class UserSource(CSVSource):
    """User Data Source.

    Implementation for the "Adult Census Income" dataset.
    Provides function to read in csv data.

    Args:
        filepath (:obj:`str`): Absolute path to the CSV file.
    """

    def __init__(self, filepath):
        super().__init__(filepath)

        self.approach_for_missing_feature = 'imputation'  # 'imputation',
        # 'dropping'
        self.imputation_method_for_cat_feats = 'unknown'  # 'unknown',
        # 'most_common_cat'
        self.imputation_method_for_quant_feats = 'median'  # 'median', 'mean'
        self.features_to_drop_list = None

        # folder with the data files
        # self.input_folder = '../dq0-sdk/dq0sdk/data/csv/census/data/'

    def read(self):
        """Read Adult dataset.

        Returns:
            data as pandas dataframe.

        Raises:
            IOError: if filepath was not found
        """
        logger.debug('Loading "Adult Census Income" dataset from file' + ''
                     '' + self.filepath)
        dataset_df = self._load_input_dataset(self.filepath)
        # util.print_dataset_info(dataset_df, 'Raw dataset')

        return dataset_df

    def _load_input_dataset(self, dataset_file_path, skiprows=None):

        # logger.debug('Load dataset from file "' + dataset_file_path + '" ')
        column_names_list = [
            'firstname',
            'lastname',
            'age',
            'workclass',
            'fnlwgt',
            'education',
            'education-num',
            'marital-status',
            'occupation',
            'relationship',
            'race',
            'sex',
            'capital-gain',
            'capital-loss',
            'hours-per-week',
            'native-country',
            'income'
        ]

        # self.categorical_features_list = [
        #    'workclass',
        #    'fnlwgt',
        #    'education',
        #    'education-num',
        #    'marital-status',
        #    'occupation',
        #    'relationship',
        #    'race',
        #    'sex',
        #    'native-country'
        # ]

        self.target_feature = 'income'

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        # quantitative_features_list = list(set(column_names_list) -
        #                                 set(self.categorical_features_list) -
        #                                 set([self.target_feature]))

        # To speed up load of data in RAM and to optimize memory consumption.
        # Not really sensible effect if dataset size is limited.
        # columns_dtype_dict = {
        #                    'age': np.uint8,
        #                    'workclass': object,
        #                    'fnlwgt': np.uint32,
        #                    'education': object,
        #                    'education-num': np.uint8,
        #                    'marital-status': object,
        #                    'occupation': object,
        #                    'relationship': object,
        #                    'race': object,
        #                    'sex': object,
        #                    'capital-gain': np.uint32,
        #                    'capital-loss': np.uint32,
        #                    'hours-per-week': np.uint8,
        #                    'native-country': object,
        #                    'income': object
        #                    }

        # Let Python decide for column types, since they may be missing values.
        dataset_df = pd.read_csv(dataset_file_path,
                                 names=column_names_list,
                                 sep=',',
                                 # false_values=['f', 'false'],
                                 # true_values=['t', 'true'],
                                 # dtype=columns_dtype_dict,
                                 skiprows=skiprows,
                                 index_col=None,
                                 # comment='|',  # dataset has comment in it
                                 # comment is in the first row only. Ignored by
                                 # setting parameter "skiprows"
                                 skipinitialspace=True,  # skip spaces after
                                 # delimiter
                                 na_values={
                                     'capital-gain': 99999,
                                     'capital-loss': 99999,
                                     'hours-per-week': 99,
                                     'workclass': '?',
                                     'native-country': '?',
                                     'occupation': '?'
                                 }
                                 # missing values in categorical features are
                                 # encoded via '?'.
                                 )

        dataset_df.drop(['lastname', 'firstname'], axis=1, inplace=True)
        column_names_list.remove('lastname')
        column_names_list.remove('firstname')

        self.categorical_features_list = [
            column for column in dataset_df.columns
            if column != self.target_feature and dataset_df[column].dtype == 'object'
        ]

        # List difference. Warning: in below operation, set does not preserve
        # the order. If order matters, use, e.g., list comprehension.
        self.quantitative_features_list = list(
            set(column_names_list) - set(self.categorical_features_list) - set([
                self.target_feature])
        )

        return dataset_df

    def _keep_selected_quantitative_features_only(self, X_df):
        selected_quantitative_feats_list = [
            'age',
            'education-num',
            'capital-gain',
            'capital-loss',
            'hours-per-week'
        ]

        X_df = X_df[selected_quantitative_feats_list + self.categorical_features_list]

        self.quantitative_features_list = selected_quantitative_feats_list

        print('\nKeep only a subset of quantitative features. The '
              'following features survived the cut:')
        util.pretty_print_strings_list(self.quantitative_features_list,
                                       'quantitative features')
        util.pretty_print_strings_list(self.categorical_features_list,
                                       'categorical features')

        return X_df

    def preprocess(self):
        """Read and preprocess the dataset.

        Returns:
            the prerocessed dataset as a pandas dataframe.
        """
        import sklearn.preprocessing

        X_df = self.read()

        logger.debug('Preprocessing "Adult Census Income" dataset')
        # print('\n\n--------- Data preprocessing ---------')
        # 1. impute missing values with data or remove missing values.
        #    According to the adult.names file, unknown values are encoded
        #    via the "?" string.
        # 2. drop uninformative features (given the remaining features)
        # 3. encode the categorical features as numeric data via one-hot
        #    encoding

        logger.debug('Handling instances with missing values')
        X_df = preprocessing.handle_missing_data(
            X_df,
            mode=self.approach_for_missing_feature,
            imputation_method_for_cat_feats=self.imputation_method_for_cat_feats,
            imputation_method_for_quant_feats=self.imputation_method_for_quant_feats,
            categorical_features_list=self.categorical_features_list,
            quantitative_features_list=self.quantitative_features_list
        )

        if self.features_to_drop_list is not None:
            X_df.drop(self.features_to_drop_list, axis=1, inplace=True)
            util.pretty_print_strings_list(
                self.features_to_drop_list,
                '\nThe following features have been dropped:')

            self.quantitative_features_list = list(
                set(self.quantitative_features_list) - set(self.features_to_drop_list)
            )

            self.categorical_features_list = list(
                set(self.categorical_features_list) - set(self.features_to_drop_list)
            )

        if self.categorical_features_list:
            logger.debug('Convert categorical features to numerical representations'
                         ' by one-hot encoding')
            #
            # (Weak) assumption: for each categorical feature, its values in
            # the test set is already present in the training set.
            #
            X_df = pd.get_dummies(X_df, columns=self.categorical_features_list,
                                  dummy_na=False)  # True => add a column to
            # indicate NaNs. False => NaNs are ignored.
            #
            # Rather than get_dummies, it would be better as follows ...
            # enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
            # enc.fit(X_df[self.categorical_features_list])

            self.categorical_features_list = []
            self.quantitative_features_list = X_df.columns.tolist()

            util.pretty_print_strings_list(
                X_df.columns.tolist(),
                'After one-hot encoding categorical features, the features are'
            )

        # label target
        y_ts = X_df[self.target_feature]
        le = sklearn.preprocessing.LabelEncoder()
        y_bin_nb = le.fit_transform(y_ts)
        y_bin = pd.Series(index=y_ts.index, data=y_bin_nb)
        X_df.drop([self.target_feature], axis=1, inplace=True)
        X_df[self.target_feature] = y_bin

        return X_df

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
