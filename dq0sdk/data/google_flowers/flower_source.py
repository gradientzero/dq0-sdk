# -*- coding: utf-8 -*-
"""Data Source abstract base class

The source class serves as the base class for all dq0sdk data sources.

Implementing subclasses have to define at least read

:Authors:
    Jona Boeddinhaus <jb@gradient0.com>
    Wolfgang Groß <wg@gradient0.com>
    Artur Susdorf <as@gradient0.com>

Copyright 2019, Gradient Zero
All rights reserved
"""


import logging
import os
import sys
import tarfile
from random import sample

from dq0sdk.data.source import Source

import numpy as np

import tensorflow as tf

logger = logging.getLogger()

root_dir = os.getcwd()

np.random.seed(1)


class FlowerSource(Source):
    """Abstract base class for all data connector sources
    available through the SDK.

    Data sources classes provide a read method to read the data into memory or
    provide a data reader for the underlying source.
    """
    def __init__(self, paths):
        super().__init__(input_folder=None)
        self.data = None
        self.preprocessed_data = None
        self.read_allowed = False
        self.meta_allowed = False
        self.types_allowed = False
        self.stats_allowed = False
        self.sample_allowed = False

        self.n_classes = 5

        try:
            self.path_train, self.path_test = paths.split(';')
        except Exception as e:
            logger.error('Problem with paths: {}'.format(e))
            sys.exit(1)

        if not os.path.exists(self.path_train):
            self.read()

    def read(self):
        """Read data sources

        This function should be used by child classes to read data or return
        a data handler to read streaming data.

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            data read from the data source.
        """
        def _move_files(origin_dir, dest_dir, test=False):
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

        tar_file = os.path.join(root_dir, 'dq0sdk/data/google_flowers/flower_photos.tgz')

        if not os.path.isfile(tar_file):
            tf.keras.utils.get_file(
                tar_file,
                'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
                extract=False)

        tar_dir = tar_file.split('.tgz')[0]
        if not os.path.exists(tar_dir):
            os.mkdir(tar_dir)
            os.mkdir(self.path_train)
            os.mkdir(self.path_test)

            my_tar = tarfile.open(tar_file)
            my_tar.extractall(os.path.split(tar_dir)[0])

            # Move all files to train
            _move_files(tar_dir, self.path_train, test=False)

            # Move subset to test
            _move_files(self.path_train, self.path_test, test=True)

    def preprocess(self):
        """Preprocess the data

        This function should be used by child classes to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            force (bool): True to force re-read of the data.
            kwargs (:obj:`dict`): dictionary of optional arguments.

        Returns:
            data read from the data source.
        """
        raise NotImplementedError()

    def to_json(self):
        """Returns a json representation of this data sources information.

        Returns:
            data source description as json.
        """
        raise NotImplementedError()
