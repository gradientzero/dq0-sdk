import os
import numpy as np
from random import sample
import tensorflow as tf
import tarfile

np.random.seed(1)

root_dir=os.getcwd()

def get_im_clf_example_data():
    tar_file = os.path.join(root_dir,'dq0sdk/data/google_flowers/flower_photos.tgz')
    train_data_dir = os.path.join(root_dir,'dq0sdk/data/google_flowers/train')
    test_data_dir = os.path.join(root_dir,'dq0sdk/data/google_flowers/test')

    if not os.path.isfile(tar_file):
        tf.keras.utils.get_file(
            tar_file,
            'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
            extract=False)
        
    tar_dir = tar_file.split('.tgz')[0]
    if not os.path.exists(tar_dir):
        os.mkdir(tar_dir)
        os.mkdir(train_data_dir)
        os.mkdir(test_data_dir)

        my_tar = tarfile.open(tar_file)
        my_tar.extractall(os.path.split(tar_dir)[0])
    
        # Move all files to train
        for subdir in os.listdir(tar_dir):
            if subdir not in ['LICENSE.txt']:
                path_train_name = os.path.join(train_data_dir,subdir)
                path_origin_name = os.path.join(tar_dir,subdir)
                if not os.path.exists(path_train_name):
                    os.mkdir(path_train_name)
                    for f in os.listdir(path_origin_name):
                        os.rename(os.path.join(path_origin_name,f), os.path.join(path_train_name,f))
                
        # Move subset to test
        for subdir in os.listdir(train_data_dir):
            if subdir not in ['LICENSE.txt']:
                path_test_name = os.path.join(test_data_dir,subdir)
                path_origin = os.path.join(train_data_dir,subdir)
                if not os.path.exists(path_test_name):
                    os.mkdir(path_test_name)
                    files_to_move=sample(os.listdir(path_origin),32*5)
                    for f in files_to_move:
                        os.rename(os.path.join(path_origin,f), os.path.join(path_test_name,f))
