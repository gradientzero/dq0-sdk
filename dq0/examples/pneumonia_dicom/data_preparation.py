# -*- coding: utf-8 -*-
"""Create feature vector for the Pneumonia DICOM dataset.
Data can be downloaded here: https://www.kaggle.com/c/rsna-pneumonia-detection-challenge/data

Copyright 2021, Gradient Zero
All rights reserved
"""

import tensorflow as tf
import pydicom
import pathlib
import os
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib import pyplot as plt
# import cv2
import seaborn as sns
from tqdm import tqdm
from sklearn import preprocessing, model_selection


parent_dir = pathlib.Path(__file__).parent.resolve()
# FOLDER_PATH = os.path.join(parent_dir, '../../../../data/RSNA_Pneunomia/rsna-pneumonia-detection-challenge/stage_2_train_images/')
FOLDER_PATH = os.path.join(parent_dir, '../../../../data/RSNA_Pneunomia/rsna-pneumonia-detection-challenge/stage_2_test_images/')


def show_dcm_info(dicom_file):
    print("Filename.........:", file_path)
    print("Storage type.....:", dicom_file.SOPClassUID)
    print()

    pat_name = dicom_file.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patient's name......:", display_name)
    print("Patient id..........:", dicom_file.PatientID)
    print("Patient's Age.......:", dicom_file.PatientAge)
    print("Patient's Sex.......:", dicom_file.PatientSex)
    print("Modality............:", dicom_file.Modality)
    print("Body Part Examined..:", dicom_file.BodyPartExamined)
    print("View Position.......:", dicom_file.ViewPosition)

    if 'PixelData' in dicom_file:
        rows = int(dicom_file.Rows)
        cols = int(dicom_file.Columns)
        print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
            rows=rows, cols=cols, size=len(dicom_file.PixelData)))
        if 'PixelSpacing' in dicom_file:
            print("Pixel spacing....:", dicom_file.PixelSpacing)


def plot_pixel_array(dicom_file, figsize=(10, 10)):
    plt.figure(figsize=figsize)
    plt.imshow(dicom_file.pixel_array, cmap=plt.cm.bone)
    plt.show()


def show_sample_data():
    i = 1
    num_to_plot = 5
    for file_name in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, file_name)
        dicom_file = pydicom.dcmread(file_path)
        show_dcm_info(dicom_file)
        plot_pixel_array(dicom_file)

        if i >= num_to_plot:
            break

        i += 1


def dataset_from_pixel_array(folder_path):
    image_ds = []
    label_ds = []
    for file_name in tqdm(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        dicom_file = pydicom.dcmread(file_path)

        image_ds.append(dicom_file.pixel_array)
        label_ds.append(dicom_file.PatientSex)  # arbitrary field selected a label

    image_ds = np.array(image_ds)
    label_ds = np.array(label_ds).reshape(-1, 1)

    ohe = preprocessing.OneHotEncoder()
    label_ds = ohe.fit_transform(label_ds).toarray()

    # train test split of the dataset
    X_train, X_test, y_train, y_test = model_selection.train_test_split(image_ds, label_ds, test_size=0.1)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    # show_sample_data()
    X_train, X_test, y_train, y_test = dataset_from_pixel_array(FOLDER_PATH)
    print("X_train.shape", X_train.shape)
    print("X_test.shape", X_test.shape)
    print("y_train.shape", y_train.shape)
    print("y_test.shape", y_test.shape)
