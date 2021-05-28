from dq0.sdk.data.base_preprocess import BasePreprocess

class CalledWhatever(BasePreprocess):
    def __init__(self):
        super().__init__()
        self.per_feature_imputation_value_ts = None
        self.categories = 'auto'
        self.ohe_params = None
        self.scaler_params = None
        self.le_params = None
        
        # columns
        self.column_names_list = [
            'lastname',
            'firstname',
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

        self.columns_types_list = [
            {
                'name': 'age',
                'type': 'int'
            },
            {
                'name': 'workclass',
                'type': 'string',
                'values': [
                    'Private',
                    'Self-emp-not-inc',
                    'Self-emp-inc',
                    'Federal-gov',
                    'Local-gov',
                    'State-gov',
                    'Without-pay',
                    'Never-worked',
                    'Unknown'
                ]
            },
            {
                'name': 'fnlwgt',
                'type': 'int'
            },
            {
                'name': 'education',
                'type': 'string',
                'values': [
                    'Bachelors',
                    'Some-college',
                    '11th',
                    'HS-grad',
                    'Prof-school',
                    'Assoc-acdm',
                    'Assoc-voc',
                    '9th',
                    '7th-8th',
                    '12th',
                    'Masters',
                    '1st-4th',
                    '10th',
                    'Doctorate',
                    '5th-6th',
                    'Preschool'
                ]
            },
            {
                'name': 'education-num',
                'type': 'int'
            },
            {
                'name': 'marital-status',
                'type': 'string',
                'values': [
                    'Married-civ-spouse',
                    'Divorced',
                    'Never-married',
                    'Separated',
                    'Widowed',
                    'Married-spouse-absent',
                    'Married-AF-spouse'
                ]
            },
            {
                'name': 'occupation',
                'type': 'string',
                'values': [
                    'Tech-support',
                    'Craft-repair',
                    'Other-service',
                    'Sales',
                    'Exec-managerial',
                    'Prof-specialty',
                    'Handlers-cleaners',
                    'Machine-op-inspct',
                    'Adm-clerical',
                    'Farming-fishing',
                    'Transport-moving',
                    'Priv-house-serv',
                    'Protective-serv',
                    'Armed-Forces',
                    'Unknown'
                ]
            },
            {
                'name': 'relationship',
                'type': 'string',
                'values': [
                    'Wife',
                    'Own-child',
                    'Husband',
                    'Not-in-family',
                    'Other-relative',
                    'Unmarried'
                ]
            },
            {
                'name': 'race',
                'type': 'string',
                'values': [
                    'White',
                    'Asian-Pac-Islander',
                    'Amer-Indian-Eskimo',
                    'Other',
                    'Black'
                ]
            },
            {
                'name': 'sex',
                'type': 'string',
                'values': [
                    'Female',
                    'Male'
                ]
            },
            {
                'name': 'capital-gain',
                'type': 'int'
            },
            {
                'name': 'capital-loss',
                'type': 'int'
            },
            {
                'name': 'hours-per-week',
                'type': 'int'
            },
            {
                'name': 'native-country',
                'type': 'string',
                'values': [
                    'United-States',
                    'Cambodia',
                    'England',
                    'Puerto-Rico',
                    'Canada',
                    'Germany',
                    'Outlying-US(Guam-USVI-etc)',
                    'India',
                    'Japan',
                    'Greece',
                    'South',
                    'China',
                    'Cuba',
                    'Iran',
                    'Honduras',
                    'Philippines',
                    'Italy',
                    'Poland',
                    'Jamaica',
                    'Vietnam',
                    'Mexico',
                    'Portugal',
                    'Ireland',
                    'France',
                    'Dominican-Republic',
                    'Laos',
                    'Ecuador',
                    'Taiwan',
                    'Haiti',
                    'Columbia',
                    'Hungary',
                    'Guatemala',
                    'Nicaragua',
                    'Scotland',
                    'Thailand',
                    'Yugoslavia',
                    'El-Salvador',
                    'Trinadad&Tobago',
                    'Peru',
                    'Hong',
                    'Holand-Netherlands',
                    'Unknown'
                ]
            }
        ]

        self.na_values_d = {
            'capital-gain': 99999,
            'capital-loss': 99999,
            'hours-per-week': 99,
            'workclass': '?',
            'native-country': '?',
            'occupation': '?'}
        
        # define target feature
        self.target_feature = 'income'

    def run(self, x, y=None, train=False):
        """Preprocess the data

        Preprocess the data set. The input data is read from the attached source.

        At runtime the selected datset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling `setup_data()`.

        Use `self.data_source.read()` to read the attached data.

        Returns:
            preprocessed data
        """
        # from dq0.sdk.data.preprocessing import preprocessing
        import sklearn.preprocessing
        import pandas as pd
        import numpy as np

        column_names_list = self.column_names_list
        columns_types_list = self.columns_types_list

        x.columns = column_names_list[:-1]

        # Do the same NaN value substitution as in read_csv
        x.replace(to_replace=self.na_values_d, value=np.nan, inplace=True)

        # drop unused columns
        x.drop(['lastname', 'firstname'], axis=1, inplace=True)
        # column_names_list.remove('lastname')
        # column_names_list.remove('firstname')

        # get categorical features
        categorical_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'string']

        # get quantitative features
        quantitative_features_list = [
            col['name'] for col in columns_types_list
            if col['type'] == 'int' or col['type'] == 'float']

        # Impute cat nan values
        x[categorical_features_list] = x[
                    categorical_features_list].fillna('Unknown')
        
        # impute numeric nan values
        if train:
            self.per_feature_imputation_value_ts = \
                        x[quantitative_features_list].median(axis=0)
        
        x[quantitative_features_list] = x[
                quantitative_features_list].fillna(
                self.per_feature_imputation_value_ts, axis=0)

        # get dummy columns
        enc = sklearn.preprocessing.OneHotEncoder(categories=self.categories, sparse=False, handle_unknown='ignore')
        enc.fit(x[categorical_features_list])
        if train:
            self.categories = enc.categories_
            self.ohe_params = enc.get_params()
        enc.set_params(**self.ohe_params)
        x_dummies = enc.transform(x[categorical_features_list])
        col_names = enc.get_feature_names(categorical_features_list)
        x_dummies = pd.DataFrame(x_dummies, columns=col_names)
        x = pd.concat([x.reset_index(drop=True), x_dummies], axis=1)
        x.drop(categorical_features_list, axis=1, inplace=True)

        # Scale values to the range from 0 to 1 to be precessed by the neural network
        scaler = sklearn.preprocessing.MinMaxScaler()
        scaler.fit(x[quantitative_features_list])
        if train:
            self.scaler_params = scaler.get_params()
        if self.scaler_params is not None:
            scaler.set_params(**self.scaler_params)
        else:
            raise ValueError('self.scaler_params cannot be None')
        x[quantitative_features_list] = scaler.transform(x[quantitative_features_list])
       
        # label target
        if y is not None:
            le = sklearn.preprocessing.LabelEncoder()
            le.fit(y)
            if train:
                self.le_params = le.get_params()
                print(le.classes_)
                print(self.le_params)
            if self.le_params is not None:
                le.set_params(**self.le_params)
            else:
                raise ValueError('self.le_params cannot be None')
        
            y = le.transform(y)

        # x.to_csv('/Users/cl/Documents/projects/gradient0/dq0-sdk/dq0/examples/census/_data/X_{}.csv'.format(train))

        return x, y
