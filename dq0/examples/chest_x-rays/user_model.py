# -*- coding: utf-8 -*-
"""Chest x-rays dataset example.

Use this class to train a Neural Network classifier on chest x-rays image data.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging
import os

import Augmentor

import cv2

from dq0.sdk.errors.errors import fatal_error
from dq0.sdk.models.tf import NeuralNetworkClassification

from imutils import paths

import numpy as np

from sklearn.model_selection import train_test_split

import tensorflow.compat.v1 as tf


logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """
    Convolutional Neural Network model implementation for chest x-rays image
    data.

    SDK users instantiate this class to create and train Keras models or
    subclass this class to define custom neural networks.

    """

    def __init__(self):
        super().__init__()
        self._classifier_type = 'cnn'
        self.label_encoder = None

    def setup_model(self, **kwargs):
        """Setup model function

        Define the CNN model.
        """
        print('Setting up a convolution neural network...')
        self._define_CNN_architecture()

        # compile model
        for layer in self.baseModel.layers:
            layer.trainable = False

        learning_rate = 1e-3
        self.epochs = 15
        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=learning_rate, decay=learning_rate / self.epochs)
        self.batch_size = 8
        self.metrics = ['accuracy']
        self.loss = tf.keras.losses.CategoricalCrossentropy()

    def _define_CNN_architecture(self):
        self.baseModel = tf.keras.applications.VGG16(
            weights="imagenet",
            include_top=False,
            input_tensor=tf.keras.layers.Input(shape=(224, 224, 3))
        )

        # construct the head of the model that will be placed on top of the
        # base model
        head_model = self.baseModel.output
        head_model = tf.keras.layers.AveragePooling2D(pool_size=(4,
                                                                 4))(head_model)
        head_model = tf.keras.layers.Flatten(name="flatten")(head_model)
        head_model = tf.keras.layers.Dense(128, activation="relu")(head_model)
        head_model = tf.keras.layers.Dense(64, activation="relu")(head_model)
        head_model = tf.keras.layers.Dropout(0.5)(head_model)
        head_model = tf.keras.layers.Dense(3, activation="softmax")(head_model)

        self.model = tf.keras.models.Model(inputs=self.baseModel.input,
                                           outputs=head_model)

        self.model.summary()

    def setup_data(self, **kwargs):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected dataset is attached to this model. It
        is available as the `data_source` attribute.

        For local testing call `model.attach_data_source(some_data_source)`
        manually before calling setup_data()`.

        Use `self.data_source.read()` to read the attached data.
        """
        # get the input dataset
        if self.data_source is None:
            fatal_error('No data source found', logger=logger)

        _ = self.data_source.read()

        self.image_classes = ['NORMAL', 'PNEUMONIA', 'COVID']
        # load data straight into UserModel
        data_path = '/Users/paolo/Documents/tasks_at_G0/DQ0/use_cases' \
                    '/UC1 - utility loss/data/'

        # recursively list path to images based on a root directory
        # see: https://github.com/PyImageSearch/imutils
        image_paths_per_class = [list(paths.list_images(
            data_path + 'input/COVID-ChestXray-15k-dataset/' + image_class)
        ) for image_class in self.image_classes]
        # list of three lists, one per class. Each of the three list contains a
        # list of files and folders.

        dataset, labels = self._preprocess_images(image_paths_per_class,
                                                  data_path=data_path)
        # dataset is a np array of 3-dims np arrays (since RGB images)
        # labels is a 1-dims np array

        # convert integer-valued labels to one-hot encoding
        labels = tf.keras.utils.to_categorical(labels)

        (self.X_train, self.X_test, self.Y_train, self.Y_test) = train_test_split(
            dataset, labels, test_size=0.20, stratify=labels)
        (self.X_train, self.X_val, self.Y_train, self.Y_val) = train_test_split(
            self.X_train, self.Y_train, test_size=0.20, stratify=labels)

    def _preprocess_images(self, image_paths_per_class,
                           save_preproc_images=False, data_path='./data/'):
        class_label = 0
        for image_paths_list in image_paths_per_class:
            class_images, class_labels = _load_and_resize_images(
                image_paths_list, label=class_label)
            if class_label == 0:
                dataset = class_images
                labels = class_labels
            else:
                dataset = np.concatenate((dataset, class_images), axis=0)
                labels = np.concatenate((labels, class_labels), axis=0)
            class_label += 1

        if save_preproc_images:
            _save_preprocessed_images(
                dataset, labels, self.image_classes,
                path_to_folder=data_path + 'output/preproc_images/'
            )

        dataset = np.array(dataset) / 255

        return dataset, labels


def _images_augmentation(path_to_data, num_of_samples=580):

    p = Augmentor.Pipeline(path_to_data)
    # add operations to a pipeline
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
    p.flip_left_right(probability=1)
    p.process()

    p.sample(num_of_samples)  # generate 580 augmented images based on above
    # specifications. Newly generated, augmented images will by default be
    # saved into a directory named "output", relative to the directory that
    # contains the initial image data set.


def _load_and_resize_images(image_paths_list, label=0):
    # recursively list path to images based on a root directory
    # image_paths_list = list(paths.list_images(normal))
    images = []
    labels = []
    for image_path in image_paths_list:
        # 224x224 pixels, ignore aspect ratio
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        # update images and labels lists, respectively
        images.append(image)
        labels.append(label)
    images = np.array(images)
    labels = np.array(labels)

    return images, labels


def _save_preprocessed_images(dataset, labels, image_classes,
                              path_to_folder='./data/output/preproc_images/',
                              rescale_before_saving=False):

    overwrite = True

    for class_name in image_classes:
        path_to_class_folder = os.path.join(path_to_folder, class_name)
        if os.path.isdir(path_to_class_folder):
            if not overwrite:
                raise RuntimeError("Folder " + path_to_class_folder +
                                   " already exists!")
        else:
            os.makedirs(path_to_class_folder)

    for c, img in enumerate(dataset):

        path_to_class_folder = os.path.join(path_to_folder, image_classes[labels[c]])

        path_to_file = os.path.join(path_to_class_folder, 'chest_xrays_' +
                                    str(c + 1) + '.jpg')

        if rescale_before_saving:
            img = np.around(img * 255)
        status = cv2.imwrite(path_to_file, img)

        if not status:
            raise RuntimeError('Failure in saving image ' + path_to_file)
