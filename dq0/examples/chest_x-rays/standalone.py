
import os
import random

import Augmentor

import cv2

from imutils import paths

from matplotlib import pyplot as plt

import numpy as np

from sklearn.model_selection import train_test_split

import tensorflow.compat.v1 as tf


debugging = True


class UserModel_mockup:

    def setup_data(self):

        data_path = '/Users/paolo/Documents/tasks_at_G0/DQ0/use_cases' \
                    '/UC1 - utility loss/data/'

        self.image_classes = ['NORMAL', 'PNEUMONIA', 'COVID']

        # file_names_per_class = [os.listdir(
        # data_path + 'input/COVID-ChestXray-15k-dataset/' + image_class)
        # for image_class in image_classes]
        #
        # recursively list path to images based on a root directory
        # see: https://github.com/PyImageSearch/imutils
        image_paths_per_class = [list(paths.list_images(
            data_path + 'input/COVID-ChestXray-15k-dataset/' +
            image_class)) for image_class in self.image_classes]
        # list of three lists, one per class. Each of the three list contains a
        # list of files and folders.

        if debugging:
            for c in range(len(image_paths_per_class)):
                image_paths_per_class[c] = image_paths_per_class[c][:50]
            for c in range(len(image_paths_per_class)):
                print(len(image_paths_per_class[c]))

        _visual_check(image_paths_per_class, self.image_classes)

        dataset, labels = self._preprocess_images(image_paths_per_class,
                                                  data_path=data_path)
        # dataset is a np array of 3-dims np arrays (since RGB images)
        # labels is a 1-dims np array

        # convert integer-valued labels to one-hot encoding
        labels = tf.keras.utils.to_categorical(labels)

        (self.X_train, self.X_test, self.Y_train, self.Y_test) = train_test_split(
            dataset, labels, test_size=0.20, stratify=labels)
        (self.X_train, self.X_val, self.Y_train, self.Y_val) = train_test_split(
            self.X_train, self.Y_train, test_size=0.20)

    def _preprocess_images(self, image_paths_per_class,
                           save_preproc_images=True, data_path='./data/'):
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

    def setup_model(self, **kwargs):
        """Setup model function

        Define the CNN model.
        """
        self._define_CNN_architecture()

        # compile model
        for layer in self.baseModel.layers:
            layer.trainable = False

        learning_rate = 1e-3
        self.epochs = 2  # 15    TODO restore 15!!!
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
        head_model = tf.keras.layers.AveragePooling2D(
            pool_size=(4, 4))(head_model)
        head_model = tf.keras.layers.Flatten(name="flatten")(head_model)
        head_model = tf.keras.layers.Dense(128, activation="relu")(head_model)
        head_model = tf.keras.layers.Dense(64, activation="relu")(head_model)
        head_model = tf.keras.layers.Dropout(0.5)(head_model)
        head_model = tf.keras.layers.Dense(3, activation="softmax")(head_model)

        self.model = tf.keras.models.Model(inputs=self.baseModel.input,
                                           outputs=head_model)

        self.model.summary()


def _visual_check(image_paths_per_class, image_classes):

    for c, image_paths_list in enumerate(image_paths_per_class):

        image_paths_list = random.sample(image_paths_list, 6)
        fig = plt.figure(figsize=(16, 12))

        for fc, image_path in enumerate(image_paths_list):
            ax = fig.add_subplot(2, 3, fc + 1)
            img = plt.imread(image_path)
            ax.imshow(img, cmap='gray')
            plt.axis(False)
        fig.suptitle(
            image_classes[c].lower().capitalize() + ' x-ray images')
        plt.show()


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


def _train_network_TBD(model):

    model.model.compile(loss=model.loss, optimizer=model.optimizer,
                        metrics=model.metrics)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=8),
        tf.keras.callbacks.ModelCheckpoint(
            filepath='../../../../../use_cases/UC1 - utility loss/best_model.h5', monitor='val_loss',
            save_best_only=True)
    ]

    # train the head of the network
    H = model.model.fit(model.X_train, model.Y_train,
                        validation_data=(model.X_val, model.Y_val),
                        batch_size=model.batch_size, epochs=model.epochs,
                        callbacks=callbacks)

    acc = H.history['accuracy']
    loss = H.history['loss']
    val_loss = H.history['val_loss']
    val_acc = H.history['val_accuracy']
    epochs = range(len(H.epoch))

    title1 = 'Accuracy and validation accuracy'
    leg1 = ['Acc', 'Val_acc']
    title2 = 'loss and validation loss'
    leg2 = ['Loss', 'Val_loss']

    def plot(epochs, acc, val_acc, leg, title):
        plt.plot(epochs, acc)
        plt.plot(epochs, val_acc)
        plt.title(title)
        plt.legend(leg)
        plt.xlabel('epochs')

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plot(epochs, acc, val_acc, leg1, title1)
    plt.subplot(1, 2, 2)
    plot(epochs, loss, val_loss, leg2, title2)
    plt.show()


def _test_trained_model_TBD(model):

    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, \
        classification_report

    # make predictions on the testing set
    print("Evaluating network")
    predIdxs = model.model.predict(model.X_test, batch_size=model.batch_size)
    integer_pred_labels = np.argmax(predIdxs, axis=1)
    # the inverse of to_categorical is numpy.argmax or Keras.argmax
    integer_test_labels = model.Y_test.argmax(axis=1)

    print(classification_report(integer_test_labels, integer_pred_labels,
                                digits=2))

    # plt.figure(figsize=(16, 12))
    # cm = confusion_matrix(integer_test_labels, integer_pred_labels)
    # sns.set(font_scale=1)  # for label size
    # sns.heatmap(cm, cmap="Blues", annot=True,
    #             annot_kws={"size": 12})
    # plt.ylabel('Actual')
    # plt.xlabel('Predicted')
    # plt.show()

    fig, ax = plt.subplots(figsize=(9, 6))
    cm = confusion_matrix(integer_test_labels, integer_pred_labels)
    # self.image_classes = ['NORMAL', 'PNEUMONIA', 'COVID']
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=model.image_classes)
    disp.plot(cmap=plt.cm.Blues, ax=ax)
    ax.set_title("Confusion matrix")
    plt.show()

    total = sum(sum(cm))
    acc = (cm[0, 0] + cm[1, 1]) / total
    sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
    print("accuracy: {:.4f}".format(acc))
    print("sensitivity: {:.4f}".format(sensitivity))
    print("specificity: {:.4f}".format(specificity))

    num_test_inst = len(integer_pred_labels)
    indexes = np.arange(len(integer_pred_labels))
    acc_pred_indeces = indexes[integer_pred_labels == integer_test_labels]
    inacc_pred_indeces = indexes[integer_pred_labels != integer_test_labels]
    num_acc_preds = len(acc_pred_indeces)

    print('Num test instances:', num_test_inst,
          '\nnum accurate predictions:', num_acc_preds,
          '\tnum inaccurate predictions: ', num_test_inst - num_acc_preds)
    print('Accuracy:', round(num_acc_preds / num_test_inst * 100, 3), '%')

    _gimme_a_glimpse_of_the_preds(model, acc_pred_indeces, inacc_pred_indeces,
                                  integer_pred_labels, integer_test_labels)


def _gimme_a_glimpse_of_the_preds(model, acc_pred_indeces, inacc_pred_indeces,
                                  integer_pred_labels, integer_test_labels,
                                  num_samples=9):

    for title, indeces in {
        'accurate predictions': acc_pred_indeces,
        'inaccurate predictions': inacc_pred_indeces
    }.items():

        imidx = random.sample(list(indeces), k=num_samples)

        ncols = 3
        nrows = int(np.ceil(num_samples / ncols))
        fig, ax = plt.subplots(nrows, ncols, sharex=True, sharey=True,
                               figsize=(15, 12))
        fig.suptitle(title)

        for n in range(num_samples):
            row = int(np.floor(n / ncols))
            col = n % ncols
            ax[row, col].imshow(model.X_test[imidx[n]])
            ax[row, col].axis('off')
            ax[row, col].set_title(
                "Predicted: {}\nActual:{}".format(
                    model.image_classes[integer_pred_labels[imidx[n]]],
                    model.image_classes[integer_test_labels[imidx[n]]]
                )
            )

        plt.show()


seed = 2
# Initialize tf random generator
# get Tensorflow version (first number only)
tf_version = int(tf.__version__.split('.')[0])

print(tf_version)

np.random.seed(seed)

os.environ["PYTHONHASHSEED"] = str(seed)

# if tf_version == 1:
#     # tf.set_random_seed(seed)  deprecated
#     tf.compat.v1.set_random_seed(seed)
# elif tf_version > 1:
#     tf.random.set_seed(seed)

tf.compat.v1.set_random_seed(seed)

# sp.random.seed(seed)
random.seed(seed)

print('\n\nPRNG seeded with value ', seed, '\n')

u = UserModel_mockup()
u.setup_data()

u.setup_model()

# debugging. TODO remove
_train_network_TBD(u)
_test_trained_model_TBD(u)
