import os
import numpy as np
from random import sample
import tensorflow as tf
import tarfile

np.random.seed(1)

root_dir = os.getcwd()

tar_file = os.path.join(root_dir, 'dq0sdk/data/google_flowers/flower_photos.tgz')
train_dir = os.path.join(root_dir, 'dq0sdk/data/google_flowers/train')
test_dir = os.path.join(root_dir, 'dq0sdk/data/google_flowers/test')


def move_files(origin_dir, dest_dir, test=False):
    for subdir in os.listdir(origin_dir):
        if subdir not in ['LICENSE.txt']:
            origin_dir_subdir = os.path.join(origin_dir, subdir)
            dest_dir_subdir = os.path.join(dest_dir, subdir)
            if not os.path.exists(dest_dir_subdir):
                os.mkdir(dest_dir_subdir)
                if test:
                    files_to_move = sample(os.listdir(origin_dir_subdir), 32 * 5)
                else:
                    files_to_move = os.listdir(origin_dir_subdir)
                for f in files_to_move:
                    os.rename(os.path.join(origin_dir_subdir, f), os.path.join(dest_dir_subdir, f))


def get_im_clf_example_data(tar_file=tar_file, train_dir=train_dir, test_dir=test_dir):
    """Downloads data and seprates them into train and test"""
    if not os.path.isfile(tar_file):
        tf.keras.utils.get_file(
            tar_file,
            'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
            extract=False)

    tar_dir = tar_file.split('.tgz')[0]
    if not os.path.exists(tar_dir):
        os.mkdir(tar_dir)
        os.mkdir(train_dir)
        os.mkdir(test_dir)

        my_tar = tarfile.open(tar_file)
        my_tar.extractall(os.path.split(tar_dir)[0])

        # Move all files to train
        move_files(tar_dir, train_dir, test=False)

        # Move subset to test
        move_files(train_dir, test_dir, test=True)
