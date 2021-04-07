# -*- coding: utf-8 -*-
"""Create feature vector for the Pneumonia image dataset.
In a real setting this could not be done outside of DQ0.
This should later be converted into a transform step in the project.


Copyright 2020, Gradient Zero
All rights reserved
"""

import argparse
import os

from PIL import Image

import numpy as np

import pandas as pd

import tensorflow as tf

import tensorflow_hub as hub


def create_dataset(data_path, DOWNSAMPLE=True):
    # load the images into memory, Note or course we could use a ImageGenerator from Tensorflow,
    # but to ensure compatability with DQ0, we've chosen the this simple route.
    data_path_train_normal = data_path + 'train/NORMAL/'
    imgs_train_normal = load_img_in_dir(data_path_train_normal)
    data_path_train_pneu = data_path + 'train/PNEUMONIA/'
    imgs_train_pneu = load_img_in_dir(data_path_train_pneu)
    data_path_test_normal = data_path + 'test/NORMAL/'
    imgs_test_normal = load_img_in_dir(data_path_test_normal)
    data_path_test_pneu = data_path + 'test/PNEUMONIA/'
    imgs_test_pneu = load_img_in_dir(data_path_test_pneu)
    # list to numpy array
    print("imgs_test_normal[0].shape: {}".format(imgs_test_normal[0].shape))
    print("imgs_test_normal[0].shape: {}".format(imgs_train_normal[0].shape))
    imgs_train_normal_ar = np.stack(imgs_train_normal)
    imgs_train_pneu_ar = np.stack(imgs_train_pneu)
    imgs_test_normal_ar = np.stack(imgs_test_normal)
    imgs_test_pneu_ar = np.stack(imgs_test_pneu)

    # train_test split
    idx_train = (0, len(imgs_train_normal_ar) + len(imgs_train_pneu_ar))
    idx_test = (idx_train[1], idx_train[1] + len(imgs_test_normal_ar) + len(imgs_test_pneu_ar))
    # label
    idx_train_normal = (0, len(imgs_train_normal_ar))
    idx_train_pneu = (idx_train_normal[1], idx_train_normal[1] + len(imgs_train_pneu_ar))
    idx_test_normal = (idx_train_pneu[1], idx_train_pneu[1] + len(imgs_test_normal_ar))
    idx_test_pneu = (idx_test_normal[1], idx_test_normal[1] + len(imgs_test_pneu_ar))

    # create a dataframe
    imgs = np.concatenate([imgs_train_normal_ar, imgs_train_pneu_ar, imgs_test_normal_ar, imgs_test_pneu_ar])
    imgs_df = pd.DataFrame(imgs)

    imgs_df.loc[imgs_df.index[idx_train[0]:idx_train[1]], 'split'] = 'train'
    imgs_df.loc[imgs_df.index[idx_test[0]:idx_test[1]], 'split'] = 'test'

    imgs_df.loc[imgs_df.index[idx_train_normal[0]:idx_train_normal[1]], 'label'] = 'normal'
    imgs_df.loc[imgs_df.index[idx_test_normal[0]:idx_test_normal[1]], 'label'] = 'normal'
    imgs_df.loc[imgs_df.index[idx_train_pneu[0]:idx_train_pneu[1]], 'label'] = 'pneumonial'
    imgs_df.loc[imgs_df.index[idx_test_pneu[0]:idx_test_pneu[1]], 'label'] = 'pneumonial'

    return imgs_df, idx_train, idx_test, idx_train_normal, idx_train_pneu, idx_test_normal, idx_test_pneu


def load_img_in_dir(data_folder, resize_shape=(224, 224)):
    """The images are reshaped and flattend to be used saved a CSV file"""
    imgs = []
    for f_name in os.listdir(data_folder):
        if f_name.endswith('.jpeg'):
            img = Image.open(data_folder + f_name).convert('L')
            img = img.resize(resize_shape)
            imgs.append(np.array(img).flatten())

    return imgs


def train_test_split_reshape(df, img_shape=(224, 224)):
    df_train = df[df['split'] == 'train']
    df_test = df[df['split'] == 'test']
    X_train = (df_train.drop(['split', 'label'], axis=1).values / 255.).reshape(-1, img_shape[0], img_shape[1])
    # y_train  = df_train['']
    y_train = ((df_train['label'] == 'pneumonial') * 1.).values.reshape(-1, 1)

    X_test = (df_test.drop(['split', 'label'], axis=1).values / 255.).reshape(-1, img_shape[0], img_shape[1])
    # y_train  = df_train['']
    y_test = ((df_test['label'] == 'pneumonial') * 1.).values.reshape(-1, 1)

    # the images are black and white only, but the model expects RGB, this is why we're stacking the arrays
    X_train = np.stack([X_train, X_train, X_train], axis=3)
    X_test = np.stack([X_test, X_test, X_test], axis=3)

    return X_train, X_test, y_train, y_test


def create_feature_vector(X, model_url="https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4"):
    """Uses a pretrained neural network form tf_hub to transform the given dataset X into a feature vec."""
    # depends on the selected tf hub model
    input_shape = (224, 224, 3)

    model = tf.keras.Sequential([hub.KerasLayer(model_url, trainable=False, input_shape=(input_shape))])
    optimizer = 'Adam'
    loss = tf.keras.losses.CategoricalCrossentropy()
    model.compile(optimizer, loss)
    feat_vec = model.predict(X)

    return feat_vec


def create_df(X_train_feat_vec, X_test_feat_vec, idx_train, idx_test, idx_train_normal, idx_train_pneu, idx_test_normal, idx_test_pneu):
    # create a dataframe
    X_feat_vec = np.concatenate([X_train_feat_vec, X_test_feat_vec])
    df_feat_vec = pd.DataFrame(X_feat_vec)

    df_feat_vec.loc[df_feat_vec.index[idx_train[0]:idx_train[1]], 'split'] = 'train'
    df_feat_vec.loc[df_feat_vec.index[idx_test[0]:idx_test[1]], 'split'] = 'test'

    df_feat_vec.loc[df_feat_vec.index[idx_train_normal[0]:idx_train_normal[1]], 'label'] = 'normal'
    df_feat_vec.loc[df_feat_vec.index[idx_test_normal[0]:idx_test_normal[1]], 'label'] = 'normal'
    df_feat_vec.loc[df_feat_vec.index[idx_train_pneu[0]:idx_train_pneu[1]], 'label'] = 'pneumonial'
    df_feat_vec.loc[df_feat_vec.index[idx_test_pneu[0]:idx_test_pneu[1]], 'label'] = 'pneumonial'

    return df_feat_vec


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data preparation for the ')

    parser.add_argument('--data-path', required=False,
                        type=str, dest='data_path',
                        default='/Users/wolfganggross/code/data/X_ray_pneumonia/chest_xray/')

    args, _ = parser.parse_known_args()

    data_path = args.data_path
    DOWNSAMPLE = True
    if DOWNSAMPLE:
        print("Downsampling is True. Only a fraction of ths images is used")
    img_shape = (224, 224)  # depends on the model
    print('Load images from file')
    img_df, idx_train, idx_test, idx_train_normal, idx_train_pneu, idx_test_normal, idx_test_pneu = create_dataset(data_path, DOWNSAMPLE=DOWNSAMPLE)
    X_train, X_test, y_train, y_test = train_test_split_reshape(img_df, img_shape=img_shape)
    print('Create feature vector X_train')
    X_train_feat_vec = create_feature_vector(X_train)
    print('Create feature vector X_test')
    X_test_feat_vec = create_feature_vector(X_test)
    print("X_train_feat_vec.shape: {}".format(X_train_feat_vec.shape))
    print("X_test_feat_vec.shape: {}".format(X_test_feat_vec.shape))
    df_feat_vec = create_df(X_train_feat_vec, X_test_feat_vec, idx_train, idx_test, idx_train_normal, idx_train_pneu, idx_test_normal, idx_test_pneu)
    # sample from all images
    if DOWNSAMPLE:
        df_feat_vec = df_feat_vec.sample(n=int(len(df_feat_vec) / 100))
    print(sum(df_feat_vec['split'] == 'test'))
    print("f_feat_vec.shape: {}".format(df_feat_vec.shape))
    df_feat_vec.to_csv(data_path + 'feat_vec_imgs.csv', index=False)
