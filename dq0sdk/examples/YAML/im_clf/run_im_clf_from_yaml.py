# -*- coding: utf-8 -*-
"""
Example of transfer learning for image classification
using a pretrained feature_vector model from
tensorflow hub, namely, MobileNet stripped of classifier layer.

Note: the download of the data for this example can take several minutes
but it only does it once

@author: Craig Lincoln <cl@gradient0.com>
"""
import logging

import os
from dq0sdk.data.google_flowers.flower_source import FlowerSource
from dq0sdk.models.tf.neural_network_yaml_image_classification import NeuralNetworkYamlImageClassification

import tensorflow as tf

tf.random.set_seed(0)

logger = logging.getLogger()


if __name__ == '__main__':
    # data paths.
    path = 'dq0sdk/data/google_flowers/'
    path_train = os.path.join(os.getcwd(), path, 'train')
    path_test = os.path.join(os.getcwd(), path, 'test')

    # DataSources expect only one path parameter,
    # so concatenate the paths in split them inside.
    paths = '{};{}'.format(path_train, path_test)
    
    # init data source
    dc = FlowerSource(paths)

    yaml_path = 'dq0sdk/examples/yaml/im_clf/yaml_config_image.yaml'
    model_path = 'dq0sdk/examples/yaml/im_clf/MobilNetV2_0.1.h5'

    # Create model and train
    im_clf = NeuralNetworkYamlImageClassification(model_path, yaml_path)
    im_clf.attach_data_source(dc)
    im_clf.run_all()

    # save model
    im_clf.save()

    # use a saved model and evaluate
    im_clf = NeuralNetworkYamlImageClassification(model_path, yaml_path)
    im_clf.attach_data_source(dc)
    im_clf.setup_data()
    im_clf.load()

    im_clf.test_data = False
    loss_tr, acc_tr, mse_tr = im_clf.evaluate()
    im_clf.test_data = True
    loss_te, acc_te, mse_te = im_clf.evaluate()
    print('Train  Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))

    # predict
    pred = im_clf.predict(im_clf.test_generator)
    print(pred)
