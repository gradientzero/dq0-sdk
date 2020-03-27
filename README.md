# dq0-sdk

DQ0 Software Development Kit

DQ0 is a platform for secure data storage and processing. It provides tools to perform machine learning methods on data that contain sensitive information and therefore cannot be easily released to external data science teams. DQ0 brings the calculation to the data. Models developed by data scientists can be trained on sensitive data with DQ0 in the secure data enclave. This guide describes how data scientists can start developing models using the DQ0 Platform.

The first section covers how to use the DQ0 CLI program to communicate directly with the DQ0 instance. The second section describes an alternative communication via the DQ0 SDK to be used for example in a Jupyter Notebook workspace. The third section provides information about the Data Science Dashboard, a web application that can also be used for high-level communication with the DQ0 instance.

## Prerequisites
First, two software components must be installed on the local computer in order to communicate with the DQ0 instance and to transmit models:

- DQ0 CLI - the command line interface that allows you to send commands to the DQ0 instance

- DQ0 SDK - a python package that contains classes to develop models in DQ0

To install the DQ0 CLI it is sufficient to download the binary and add the installation path to the PATH environment variable of the respective operating system. 

You can install the DQ0 SDK with the pip package manager. Use an appropriate virtual environment (i.e. Miniconda or Virtualenv) based on Python 3.7 and install the DQ0 SDK with the following command:
```bash
# will follow soon
# pip install dq0sdk

# switch to your python environment
# conda activate dq0

# clone git repository 
git clone git@github.com:gradientzero/dq0-sdk.git

# move into dq0-sdk
cd dq0-sdk

# install requirements
pip install -r requirements.txt
```

## First steps
You can call the DQ0 CLI  in an terminal (e.g. bash) with the command `dq0`. All commands of the DQ0 CLI follows the form `dq0 [context] [command] [arguments]`.

Examples:

```bash
# login to the DQ0 instance
dq0 auth login
```

```bash
# train a model
dq0 model train
```

## Register instance
When the CLI is used for the first time, the DQ0 data quarantine instance to be used must first be registered. This is done with the following command:

```bash
dq0 proxy add --scheme https --hostname [URL] --port [PORT]
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
dq0 auth register
````

You will then be asked for a user name (email address) and password.

While registering the CLI will create your personal DQ0 SSH key pair (private and public key) that will be used for the end-to-end encryption of the DQ0 communication.

*Note: All communication with the DQ0 instance is encrypted end-to-end. You can therefore only communicate with the instance from the computer with which you carried out the registration. For more information, please refer to the “DQ0-ClI User Manual”.*

The registration request must first be confirmed by your customer's DQ0 administrator. Only then can you log in with your chosen credentials using the following command:

```bash
dq0 auth login
````

In the following dialog, please enter your chosen email address and password.

After successful registration, the session is valid for 30 days.


## Projects
Working with DQ0 is about developing machine learning models for existing datasets. The first step is therefore always to create a project for a model to be developed. Enter the following command:

```bash
dq0 project create --name [PROJECT NAME]
```

Example:

```bash
dq0 project create --name model1
```

This command creates a folder with the name of your project (here “model1”) within the current directory of your terminal session. In this new folder there is a minimal Python project, which is explained in the next section.

In the project directory there is also a “.meta” file which contains the most important information about the project or the model to be developed. The CLI uses these values when communicating with the DQ0 instance if no other explicit information about them is given in the respective command. Among other things, the data source to which the model is connected is cached here (for which data source is this model developed?) And which version the model currently has.

The version of the model is an integer. It is used to track different development stages or alternatives to the model.
Tip: Use the version management git in your project directory and create a separate branch for each model version.

To set the version of the model, enter the following CLI command:

```bash
dq0 model set --version [NUMBER]
```

So to set the current status to version 2, for example:

```bash
dq0 model set --version 2
```

## Data
Models are developed for certain data sets. These data records are protected within the secure DQ0 instance. DQ0 never provides secret information about these records. However, you can of course request general information about the existing data records.

First, use the following command to get a list of all available records in quarantine:

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
dq0 data info --uuid 44b147aa-30a2-48d1-8c0b-73c9ab914c18
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
dq0 data attach --uuid [DATASET-UUID]
```

Example:

```bash
dq0 data attach --id 1
```

The command would look like this outside of the project directory:

```bash
dq0 data attach --id 1 --model [MODEL-UUID]
```


## Define the model
There are three files in the new project directory:

- run.py
- models/user_model.py
- data/user_source.py

“run.py” contains sample code to test the model to be developed locally. “models/user_model.py” defines the actual model. “data/user_source.py” defines the data source to be used and any necessary preprocessing steps.

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

from user_source import UserSource
from user_model import UserModel


if __name__ == '__main__':

    # init data source
    dc = UserSource(filepath="path/to/source")

    # create model
    model = UserModel(model_path="path/to/model")

    # attach data source
    model.attach_data_source(dc)

    # prepare data
    model.setup_data()

    # setup model
    model.setup_model()

    # fit the model
    model.fit()

    # evaluate
    model.evaluate(x=1, y=2)
```

The data source is instantiated in line 18 - in the case of a CSV data source with a path to the CSV file - and assigned to the model in line 25. The model itself is created in line 22 with a path that is used to save the model.

Line 28 calls the model's setup_data() function. This method contains your own code to prepare the data for later use in the model.

Finally, setup_model() in line 31 contains your code for defining and configuring the model itself. In the example below we see how exactly such a definition can look like.

Lines 34 and 37 call the model's fit() and evaluate() functions. DQ0 will take care of those at runtime in the quarantine. You can insert any code in these functions for test purposes, but it is ignored during the actual execution.

The template for the data source looks like this:
```python
# -*- coding: utf-8 -*-
"""User Data Source.

This is a template for user defined data sources.
When training a model on a certain deta source dq0-core is looking for a
UserSource class that is to be used as the custom data source implementation.

This template class derives from Source. Actual implementations should derive
from child classes like CSVSource.

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

import numpy as np

from dq0sdk.data.source import Source

logger = logging.getLogger()


class UserSource(Source):
    """User Data Source.

    Template. Real implementations should derive from Source child classes.
    For example: UserSource(CSVSource)

    Args:
        filepath (str): Absolute path to the data file.
    """
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def read(self, force=False):
        """Read CSV data sources

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            CSV data as pandas dataframe

        Raises:
            IOError: if file was not found
        """
        pass

    def preprocess(self, force=False):
        """Preprocess the data

        This function should be used to perform certain
        preprocessing steps to prepare the data for later use.

        Args:
            force (bool): True to force re-read of the data.

        Returns:
            preprocessed data
        """
        self.data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32")
```
The read() function in lines 37ff should normally not be implemented by yourself. Instead, following the advice in lines 27 and 28, the class should inherit from a data source definition, which already implements this read() function correctly. This would be e.g. the class “CSVSource” for reading CSV files.

You can write any code to preprocess the data in the preprocess() function from line 51. 
Note: preprocess() is executed via the dq0 data preprocess command in the DQ0 instance. The result is a new data source with the data transformed by preprocess, which is directly assigned to the model.

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

from dq0sdk.models.model import Model

from sklearn.model_selection import train_test_split

logger = logging.getLogger()


class UserModel(Model):
    """Derived from dq0sdk.models.Model class

    Model classes provide a setup method for data and model
    definitions.

    Args:
        model_path (str): Path to the model save destination.
    """
    def __init__(self, model_path):
        super().__init__(model_path)

    def setup_data(self):
        """Setup data function

        This function can be used to prepare data or perform
        other tasks for the training run.
        """
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))
        self.train_data, self.data = source.read()

        # get train and test data
        self.X_test, self.y_test = None

    def setup_model(self):
        """Setup model function

        Define the model here.
        """
        pass
```
In the setup_data() function from line 29, an assigned data source is first fetched in order to read in the data. In following lines the dataset would be prepared (split) for model training.

setup_model() from line 45 defines the model.

To define different models, the UserModel class can be derived from existing model classes in the DQ0 SDK. These include:
- `dq0sdk.models.tf.NeuralNetwork` for Neural Networks with Tensorflow and Keras.
- `dq0sdk.models.tf.NeuralNetworkYaml` for Neural Networks that will be defined by Yaml-files. These types of models can also be used for Tensorflow Hub integrations.
- `dq0sdk.models.bayes.NaiveBayesianModel` for Naïve Bayes models.


## Model Examples
The following code snippet shows an example model that works on the “adult” data record of the Census database (https://archive.ics.uci.edu/ml/datasets/Adult). The task is to classify personal entries into those with an income greater than and those with an income less than or equal to USD 50,000. The code for the data source, which reads the data, checks for missing entries and divides it into training and test data, is not listed here for the sake of clarity; however, it is included in the dq0sdk.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adult dataset example.
Neural network model definition

Copyright 2020, Gradient Zero
All rights reserved
"""

import logging

import dq0sdk
from dq0sdk.data.preprocessing import preprocessing

import pandas as pd

import sklearn
import sklearn.preprocessing

from tensorflow import keras

from sklearn.model_selection import train_test_split

logger = logging.getLogger()


class NeuralNetwork_adult(dq0sdk.models.tf.neural_network.NeuralNetwork):
    def __init__(self, model_path):
        super().__init__(model_path)
        self.learning_rate = 0.3
        self.input_dim = None

    def setup_data(self):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        data = source.read()

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
```

The parent class NeuralNetwork has further attributes which are important for the configuration of the model:

```python
class NeuralNetwork(Model):
    """Neural Network model implementation.

    SDK users can use this class to create and train Keras models or
    subclass this class to define custom neural networks.
    """
    def __init__(self, model_path):
        super().__init__(model_path)
        self.model_type = 'keras'
        self.learning_rate = 0.15
        self.epochs = 10
        self.num_microbatches = 250
        self.verbose = 0
        self.metrics = ['accuracy', 'mse']
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
```

These attributes are used at runtime in the DQ0 quarantine to build the model and conduct the training.

Additional own attributes and functions, auxiliary classes or more complex inheritance structures can be added at any time.


## Data Preprocessing
You can execute the function DataSource.preprocess within the DQ0 instance in order to transform a data source in a defined way. The result of this process is a new data source, which can also be used for the model. After calling preprocess, the transformed data is available as a new data source. The new data source is directly assigned to the current project instead of the original one.

Your preprocess() function of the UserSource class has to be transferred to the DQ0 instance with the command `dq0 project deploy` (DQ0 will always use the latest deployed version). 
The preprocessing always happens on the data record that was attached to the project with the command `dq0 data attach` (you can retrieve information about the project with `dq0 project info`).

The command to execute data preprocessing is:
```bash
dq0 data preprocess
```
The status of this job can be queried using the following command:
```bash
dq0 data state
```
The response of this command also contains the UUID of the new data source as soon as the preprocessing has been completed. The new data source will be included in the results of `dq0 data list`.

Data records that have already been preprocessed can also be preprocessed further - for example for an even more specific feature definition. Simply call `dq0 data preprocess` on the dataset that is currently attache to the project by `dq0 data attach`.


## Model Deployment and Training
If the model is now fully defined and has been tested locally (see run.py script above), it can be transferred to the DQ0 instance. This is done with the following command:

```bash
dq0 project deploy --version [NUMBER]
```

The --version argument is optional; if you omit it the curret model version will be used as stored in the .meta file. If the version is neither defined there or if you give the version “0” DQ0 will use the highest available version or 1 otherwise. 

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

*Note: only one training or prediction process can be executed at a time for one model version. If several training processes are to be executed in parallel, you have to work with different model versions (see above `dq0 model set --version 2`).*


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


# Jupyter Notebook - DQ0 SDK
The DQ0-SDK contains a sample notebook named "DQ0SDK-Demo.ipynb". This example is explained in more detail below.


## Prerequisites
Before communication with the DQ0 instnace can begin using python code, there must be a valid connection to the DQ0 proxy. To do this, follow the steps in the above sections “Register Instance” and “Log In”.

A local communication session must also be started via the DQ0 CLI. This is done with the following command:
```bash
dq0 server start
```
The DQ0 CLI program then starts a local http server that communicates with the DQ0 SDK and uses the encrypted connection to the proxy for messages to or from the quarantine. This program must be running while working with the DQ0 SDK. Should it be interrupted, the python calls to the SDK will return corresponding error messages. In this case, simply restart the local CLI server with the above command.


## Concept
The two main classes to use the DQ0 SDK to communicate with the quarantine:

- Project - the current model environment, a workspace and directory in which the models can be defined. “Project” also provides methods for accessing trained models.

- Experiment - The DQ0 runtime class to start model training in quarantine.

Start by importing these dependencies:
```python
# import dq0sdk
from dq0sdk.core import Project, Experiment
```

## Create project
First we create a project. Projects act as the environments in which the models are defined. Each project has a model directory with a .meta file. which contains the UUID of the model, connected data sources etc. Creating a model with `Project.create(name='model_1')` is equivalent to this DQ0 CLI command `dq0 model create --name model_1`

```python
# create a project with name 'model_1'. Automatically creates the 'model_1' directory and changes to this directory.
project = Project(name='model_1')
```

## Load project
Alternatively, you can load an existing project by first changing to the project directory and then call `Project.load()`. This reads in the project's .meta file to create the project instance.

```python
%cd model_1
````

```python
# Alternative: load a project from the current model directory
project = Project.load()
```

## Create experiment
To perform DQ0 model training within the quarantine, you need to create experiments. You can create as many experiments for your projects as you want.

```python
# Create experiment for project
experiment = Experiment(project=project, name='experiment_1')
```

## Attach data source
You must now connect a data source in new projects. With existing (loaded) projects, data sources are usually already connected.

```python
# import CSVSource data source class
from dq0sdk.data.csv import CSVSource

# Get or create source
data_sources = project.get_attached_sources()
if len(data_sources) > 0:
    data_source = data_sources[0]
else:
    data_source = CSVSource('data/train_test.csv')
    project.attach_source(data_source)
```

## Define a model
To define a model two functions are important:

- setup_data() - is called directly before the model training. Prepares the data source for model training.

- setup_model() - contains the actual code for the model definition.

The easiest way to define these functions is to simply write them directly in the notebook and transfer them to the Project instance. Alternatively, you can define the complete user_model.py file and save it in the model directory.


### Define functions directly in the notebook
In the first variant, the functions are defined directly in the notebook and then transferred to the project instance:

```python
import keras
from sklearn.model_selection import train_test_split

# define functions

def setup_data():
    # load data
    if len(self.data_sources) < 1:
        logger.error('No data source found')
        return
    source = next(iter(self.data_sources.values()))

    data = source.read()

    X_train_df, X_test_df, y_train_ts, y_test_ts =\
        train_test_split(data.iloc[:, :-1],
                          data.iloc[:, -1],
                          test_size=0.33,
                          random_state=42)
    self.input_dim = X_train_df.shape[1]

    # set data member variables
    self.X_train = X_train_df
    self.X_test = X_test_df
    self.y_train = y_train_ts
    self.y_test = y_test_ts
    
def setup_model():
    self.model = keras.Sequential([
        keras.layers.Input(len(kwargs['feature_columns'])),
        keras.layers.Dense(10, activation='tanh'),
        keras.layers.Dense(10, activation='tanh'),
        keras.layers.Dense(2, activation='softmax')]
    )
    
# pass them to project
project.set(setup_data=setup_data, setup_model=setup_model)

# with set you can also set the parent class
project.set(parent_class_name='NeuralNetwork', setup_data=setup_data, setup_model=setup_mo
```

### Define functions as source code
In this second variant, the source files are written directly. A template can be viewed using the following command: `!cat user_model.py` (created by `dq0 project create`).

```python
%%writefile user_model.py

import logging

from dq0sdk.models.tf.neural_network import NeuralNetwork

from sklearn.model_selection import train_test_split

from tensorflow import keras

logger = logging.getLogger()


class UserModel(NeuralNetwork):
    def __init__(self, model_path):
        super().__init__(model_path)
        self.learning_rate = 0.3
        self.epochs = 5
        self.num_microbatches = 1
        self.verbose = 0
        self.metrics = ['accuracy', 'mse']
        self.input_dim = None

    def setup_data(self):
        # load data
        if len(self.data_sources) < 1:
            logger.error('No data source found')
            return
        source = next(iter(self.data_sources.values()))

        data = source.read()

        X_train_df, X_test_df, y_train_ts, y_test_ts =\
            train_test_split(data.iloc[:, :-1],
                             data.iloc[:, -1],
                             test_size=0.33,
                             random_state=42)
        self.input_dim = X_train_df.shape[1]

        # set data member variables
        self.X_train = X_train_df
        self.X_test = X_test_df
        self.y_train = y_train_ts
        self.y_test = y_test_ts

    def setup_model(self):
        self.model = keras.Sequential([
            keras.layers.Input(self.input_dim),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(10, activation='tanh'),
            keras.layers.Dense(2, activation='softmax')])
```


## Modell training
After you have tested your model locally in the notebook, it is time to carry out the training in quarantine. This is achieved by calling `experiment.train()`, which in turn calls the CLI commands `dq0 project deploy` and `dq0 model train`.

```python
run = experiment.train()
```
A call to `train()` is asynchron. You can wait for the run to complete or get the current state with `get_state()`.

```python
# wait for completion
run.wait_for_completion(verbose=True)

# or get the state whenever you like
print(run.get_state())
```

Once the training run has been completed you can get the results:

```python
# get training results
print(run.get_results())
```

## Model predict
To call the model’s predict function do the following:

```python
import numpy as np

# get the latest model
model = project.get_latest_model()

# check DQ0 privacy clearing
if model.predict_allowed:

    # call predict
    run = model.predict(np.array([1, 2, 3]))

    # wait for completion
    run.wait_for_completion(verbose=True)

    # get training results
    print(run.get_results())
```


