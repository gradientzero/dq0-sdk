import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dq0sdk.models.tf.process_yaml_config import YamlConfig
import dq0sdk.models.tf.neural_network
from dq0sdk.examples.YAML.neural_network import NeuralNetwork_adult_yaml
import os

from dq0sdk.data.adult import AdultSource

if __name__=='__main__':

    path = 'dq0sdk/data/adult/data/'
    path_test = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.test')
    path_train = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../../../', path, 'adult.data')

    dc = AdultSource(path_test, path_train)
    train_data, data = dc.read()
    X_df, y_ts, num_tr_instances = dc.preprocess(approach_for_missing_feature='imputation',
                                                 # 'imputation', 'dropping',
                                                 imputation_method_for_cat_feats='unknown',
                                                 # 'unknown', 'most_common_cat'
                                                 imputation_method_for_quant_feats='median',  # 'median', 'mean'
                                                 features_to_drop_list=None
                                                 )

    yaml_path = 'dq0sdk/examples/YAML/yaml_config_adult.yaml'
    yaml_config = YamlConfig(yaml_path)
    model = NeuralNetwork_adult_yaml(yaml_config)
    X_train_df, X_test_df, y_train_ts, y_test_ts = model.setup_data(X_df, y_ts, dc.quantitative_features_list,
                                                                    num_tr_instances)
    model.setup_model()
    model.fit(X_train=X_train_df, y_train=y_train_ts)
    # model.fit_dp(X_train=X_train_df, y_train=y_train_ts)
    loss_tr, acc_tr, mse_te = model.evaluate(X_train_df, y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(X_test_df, y_test_ts)
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))