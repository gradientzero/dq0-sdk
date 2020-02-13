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
from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml

from tensorflow import keras

import tensorflow as tf

tf.random.set_seed(0)

logger = logging.getLogger()


class NeuralNetworkYamlFlowers(NeuralNetworkYaml):
    def __init__(self, model_path, yaml_path):
        super().__init__(model_path, yaml_path)
        self.preprocessing = self.yaml_dict['PREPROCESSING']

    def setup_data(self, augment=False):
        self.path_train = next(iter(self.data_sources.values())).path_train
        self.path_test = next(iter(self.data_sources.values())).path_test

        development_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        development_generator = development_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['development_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        if augment:
            train_datagen = keras.preprocessing.image.ImageDataGenerator(
                **self.preprocessing['datagen_kwargs'],
                **self.preprocessing['train_datagen'],)
        else:
            train_datagen = development_datagen
        train_generator = train_datagen.flow_from_directory(
            self.path_train,
            **self.preprocessing['train_dataflow'],
            **self.preprocessing['dataflow_kwargs'])

        test_datagen = keras.preprocessing.image.ImageDataGenerator(
            **self.preprocessing['datagen_kwargs'],)
        test_generator = test_datagen.flow_from_directory(
            self.path_test,
            **self.preprocessing['test_dataflow'],
            **self.preprocessing['dataflow_kwargs'],)

        # Get number of batches per epoch
        steps_per_epoch = train_generator.samples // train_generator.batch_size
        validation_steps = development_generator.samples // development_generator.batch_size
        test_steps = test_generator.samples // test_generator.batch_size

        self.n_classes = train_generator.num_classes
        self.X_train = train_generator
        self.X_validate = development_generator
        self.X_test = test_generator

        self.fit_kwargs = dict(
            steps_per_epoch=steps_per_epoch,
            validation_data=development_generator,
            validation_steps=validation_steps)
        self.eval_train_kwargs = dict(steps=steps_per_epoch)
        self.eval_test_kwargs = dict(steps=test_steps)

        # set input/oupt size
        self.graph_dict['config']['layers'][-1]['config']['units'] = self.n_classes


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
    model_path = 'dq0sdk/examples/yaml/im_clf'

    # Create model and train
    im_clf = NeuralNetworkYamlFlowers(model_path, yaml_path)
    im_clf.attach_data_source(dc)
    im_clf.run_all()

    # save model
    im_clf.save()
    im_clf.load()

    loss_tr, acc_tr, mse_tr = im_clf.evaluate(test_data=False)
    loss_te, acc_te, mse_te = im_clf.evaluate()
    print('Train  Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))

    # predict
    pred = im_clf.predict(im_clf.X_test)
    print(pred)
