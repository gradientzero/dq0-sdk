# dq0-sdk

DQ0 Software Development Kit

DQ0 is a platform for secure data storage and processing. It provides tools to perform machine learning methods on data that contain sensitive information and therefore cannot be easily released to external data science teams. DQ0 brings the calculation to the data. Models developed by data scientists can be trained on sensitive data with DQ0 in the secure data enclave. This guide describes how data scientists can start developing models using the DQ0 platform.


## Jupyter Notebook - DQ0 SDK
The DQ0-SDK contains a sample notebook named [DQ0SDK-Demo.ipynb](./dq0/sdk/notebooks/DQ0SDK-Quickstart.ipynb). Please navigate to this notebook to learn more about the DQ0 SDK usage.


## Prerequisites
First, two software components must be installed on the local computer in order to communicate with the DQ0 instance and to transmit models:

- DQ0 CLI - the command line interface that allows you to send commands to the DQ0 instance
- DQ0 SDK - a python package that contains classes to develop models in DQ0

To install the DQ0 CLI it is sufficient to download the binary and add the installation path to the PATH environment variable of the respective operating system. 

You can install the DQ0 SDK with the pip package manager. Use an appropriate virtual environment (i.e. Miniconda or Virtualenv) based on Python 3.7 and install the DQ0 SDK with the following command:
```bash
# switch to your python environment
conda activate dq0

# install dq0 sdk
pip install git+git://github.com/gradientzero/dq0-sdk.git#egg=dq0-sdk

# or clone git repository...
git clone git@github.com:gradientzero/dq0-sdk.git

# ...move into dq0-sdk...
cd dq0-sdk

# ...and install the requirements
pip install -r requirements.txt
```

## First steps
You can call the DQ0 CLI in an terminal (e.g. bash) with the command `dq0`. All commands of the DQ0 CLI follows the form `dq0 [context] [command] [arguments]`.

Examples:

```bash
# login to the DQ0 instance
dq0 user login
```

```bash
# train a model
dq0 model train
```

## Register instance
When the CLI is used for the first time, the DQ0 data quarantine instance to be used must first be registered. This is done with the following command:

```bash
dq0 proxy add --hostname [URL] --port [PORT]
````

So, for example for ‘https://dq0.io:8000’.

```bash
dq0 proxy add --hostname dq0.io --port 8000
```
Your DQ0 administrator can tell you the URL and port of your instance


## Log in
In order to communicate with the DQ0 instance, you have to log in so authorize and authenticate. 

If you are not yet registered, you can do this directly via the CLI using the following command:

```bash
dq0 user register
````

You will then be asked for a user name (email address) and password.

While registering the CLI will create your personal DQ0 SSH key pair (private and public key) that will be used for the end-to-end encryption of the DQ0 communication.

*Note: All communication with the DQ0 instance is encrypted end-to-end. You can therefore only communicate with the instance from the computer with which you carried out the registration. For more information, please refer to the “DQ0-ClI User Manual”.*

The registration request must first be confirmed by your customer's DQ0 administrator. Only then can you log in with your chosen credentials using the following command:

```bash
dq0 user login
````

In the following dialog, please enter your chosen email address and password.

After successful registration, the session is valid for 30 days.


## Projects
Working with DQ0 is about developing machine learning models for existing datasets. The first step is therefore always to create a project for a model to be developed. Enter the following command:

```bash
dq0 project create [PROJECT NAME]
```

Example:

```bash
dq0 project create model1
```

This command creates a folder with the name of your project (here “model1”) within the current directory of your terminal session. In this new folder there is a minimal Python project, which is explained in the next section.

In the project directory there is also a “.meta” file which contains the most important information about the project or the model to be developed. The CLI uses these values when communicating with the DQ0 instance if no other explicit information about them is given in the respective command. Among other things, the data source to which the model is connected is cached here (for which data source is this model developed?) And which version the model currently has.

The CLI automatically initialized and manages a local git repository for each project. Whenever you change the version of your project (e.g. to develop an alternative model version) the current git branch is created or checked out. You can let the CLI manage the git branches or do it yourself inside the project directory.

To set the version of the model, enter the following CLI command:

```bash
dq0 project set-version [VERSION-STRING]
```

## Data
Models are developed for certain data sets. These data sets are protected within the secure DQ0 instance. DQ0 never provides secret information about these records. However, you can of course request general information about the existing data sets.

First, use the following command to get a list of all available sets in quarantine:

```bash
dq0 data list
```

The result is a list of the available data sources with the information ID, UUID, name and type. A response with an existing test data record can e.g. look like this:

```bash
+----+--------------------------------------+------+------+
| ID | UUID                                 | NAME | TYPE |
+----+--------------------------------------+------+------+
|  1 | 44b147aa-30a2-48d1-8c0b-73c9ab914c18 | test | csv  |
+----+--------------------------------------+------+------+
```
The dataset with the name “test” is of type “csv” (comma separated values file); it has the ID “1” and the UUID (universally unique identifier) “44b147aa-30a2-48d1-8c0b-73c9ab914c18“.

Further information about a data record can be obtained with the following command:

```bash
dq0 data info --id [ID]
```

Example:

```bash
dq0 data info --id 1
```

Alternatively, the UUID can also be used:

```bash
dq0 data info --data-source-uuid 44b147aa-30a2-48d1-8c0b-73c9ab914c18
```

An answer comes in JSON format and can look like this:
```bash
{type: csv, size: 1000.0, mean: 55.5, std: 2.5, stats: ''}
```


## Attach data set
Once the desired data record has been found, it must be assigned to the current project. This command can be used from the project directory:

```bash
dq0 data attach --id [DATASET-ID]
```

or

```bash
dq0 data attach --data-source-uuid [DATASET-UUID]
```

Example:

```bash
dq0 data attach --id 1
```


## Define the model
There are two files in the new project directory:

- run.py
- models/user_model.py

“run.py” contains sample code to test the model to be developed locally. “models/user_model.py” defines the actual model including data preparation steps.

run.py looks like this:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run script.

Copyright 2020, Gradient Zero
All rights reserved
"""

import os

from user_model import UserModel


if __name__ == '__main__':

    # init input data source
    data_source = dq0.sdk.data.text.CSV('path/to/source')

    # create model
    model = UserModel()

    # attach data source
    model.attach_data_source(data_source)

    # prepare data
    model.setup_data()

    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate
    loss_tr, acc_tr, mse_te = model.evaluate(test_data=False)
    loss_te, acc_te, mse_te = model.evaluate()
    print('Train Acc: %.2f %%' % (100 * acc_tr))
    print('Test  Acc: %.2f %%' % (100 * acc_te))
```

The data source is instantiated in line 18 - in the case of a CSV data source with a path to the CSV file - and assigned to the model in line 24. The model itself is created in line 21 with a path that is used to save the model.

Line 27 calls the model's setup_data() function. This method contains your own code to prepare the data for later use by the model.

Finally, setup_model() in line 30 contains your code for defining and configuring the model itself. In the example below we see how exactly such a definition can look like.

Lines 33 and 36 and below call the model's fit() and evaluate() functions. DQ0 will take care of those at runtime in the quarantine. You can insert any code in these functions for test purposes, but it is ignored during the actual execution.

The template for user_model looks like this:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
User Model template
		
Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

from dq0.sdk.models.tf import NeuralNetworkClassification

logger = logging.getLogger()


class UserModel(NeuralNetworkClassification):
    """Derived from dq0.sdk.models.tf.NeuralNetworkClassification class

    Model classes provide a setup method for data and model
    definitions.
    """
    def __init__(self):
        super().__init__()

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.

        At runtime the selected datset is attached to this model. It
        is available as the data_source attribute.

        For local testing call model.attach_data_source(some_data_source)
        manually before calling setup_data().

        Use self.data_source.read() to read the attached data.
        """
        from sklearn.model_selection import train_test_split

        # get the input dataset
        if self.data_source is None:
            logger.error('No data source found')
            return

        # read the dataset from the attached input source
        data = self.data_source.read()

        # do the train test split
        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                                data.iloc[:, -1],
                                test_size=0.33,
                                random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data attributes
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        from tensorflow import keras
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
        self.optimizer = 'Adam'
        self.learning_rate = 0.015
        self.epochs = 10
        self.num_microbatches = 250
        self.verbose = 0
        self.metrics = ['accuracy', 'mse']
```
In the setup_data() function, an assigned data source is first fetched in order to read in the data. In following lines the dataset would be prepared (split) for model training.

setup_model() defines the model.

To define different models, the UserModel class can be derived from existing model classes in the DQ0 SDK. These include:
- `dq0.sdk.models.tf.NeuralNetworkClassification` for Neural Networks for classification with Tensorflow and Keras.
- `dq0.sdk.models.tf.NeuralNetworkMulticlassClassification` for Neural Networks for multiclass classification with Tensorflow and Keras.
- `dq0.sdk.models.tf.NeuralNetworkRegression` for Neural Networks for regression tasks with Tensorflow and Keras.
- `dq0.sdk.models.tf.NeuralNetworkYaml` for Neural Networks that will be defined by Yaml-files. These types of models can also be used for Tensorflow Hub integrations.
- `dq0.sdk.models.bayes.NaiveBayesianModel` for Naïve Bayes models.


## Model Deployment and Training
If the model is defined and has been tested locally (see run.py script above), it can be transferred to the DQ0 instance. This is done with the following command:

```bash
dq0 project deploy
```

After the model has been successfully transferred, a training run can be started:

```bash
dq0 model train
```

If you don’t provide additional arguments the current model version and the currently assigned data source are used.

The training process can take some time. The answer of the "train" command is therefore only a success message about the start of the training. The current status of the process can be retrieved at any time with the following command:

```bash
dq0 model state
```

A response can look like this:
```bash
State: Finished at 2020-02-17 11:12:54.405378 +0000 UTC. Progress: 1.0. Train Results: [...]. Predict Results: [...]
```

*Note: only one training or prediction process can be executed at a time for one model version. If several training processes are to be executed in parallel, you have to work with different model versions (see above `dq0 model set-version [VERSION]`).*


## Model Predict
If a model or a version of a model has been successfully trained and this model version of DQ0 has been classified as safe under data protection criteria, it can be used to predict new data. To do this, use the following command:

```bash
dq0 model predict --input-path [PATH-TO-TEST-DATA]
```
Example:

```bash
dq0 model predict --input-path predict_data.npy
```

Note that the test data must be saved in npy format. npy files are serialized numpy arrays that can be created from an np.array with the following command:

```python
import numpy as np

data = np.array([1, 2, 3])

np.save('predict_data.npy', data)
```
