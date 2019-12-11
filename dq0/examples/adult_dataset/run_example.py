import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import dq0.models.tf.neural_network
from dq0.data_connector import data_connector
from dq0.examples.adult_dataset.neural_network import NeuralNetwork_adult

if __name__=='__main__':

    path = 'dq0/data/adult/'
    dc = data_connector.Data_Connector_Adult()
    tr_dataset_df, test_dataset_df, categorical_features_list, \
                   quantitative_features_list, target_feature = dc.read_data(path)
    X_df, y_ts, num_tr_instances = dc.preprocess_dataset(tr_dataset_df, test_dataset_df,
                                       categorical_features_list, quantitative_features_list, target_feature,
                                       approach_for_missing_feature='imputation',  # 'imputation', 'dropping',
                                       imputation_method_for_cat_feats='unknown',  # 'unknown', 'most_common_cat'
                                       imputation_method_for_quant_feats='median',  # 'median', 'mean'
                                       features_to_drop_list=None
                                      )

    model = NeuralNetwork_adult(model_path='notebooks/saved_model/')
    X_train_df, X_test_df, y_train_ts, y_test_ts = model.setup_data(X_df, y_ts, quantitative_features_list,
                                                                    num_tr_instances)
    model.setup_model()
    model.fit(X_train=X_train_df, y_train=y_train_ts)
    # model.fit_dp(X_train=X_train_df, y_train=y_train_ts)
    loss_tr, acc_tr, mse_te = model.evaluate(X_train_df, y_train_ts)
    loss_te, acc_te, mse_te = model.evaluate(X_test_df, y_test_ts)
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))