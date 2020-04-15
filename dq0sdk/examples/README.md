# dq0-sdk - examples

The sample package contains several ready-to-use examples, each of which includes a user data source definition and a user model definition.

For an introduction how to use the examples, please refer to the SDK documentation, the data science getting started guide and the quickstart notebook: [DQ0SDK-Quickstart.ipynb](https://github.com/gradientzero/dq0-sdk/blob/master/dq0sdk/cli/DQ0SDK-Quickstart.ipynb)

Remember that DQ0 projects always consists of a `UserModel` class defined in `model.user_mode.py` and a `UserSource` class defined in `data.user_source.py`. Therefore all files and classes in each individual example package are named `user_model.py` / `UserModel` and `user_source.py` / `UserSource`.

The examples are based on different publicly available data sets. Data itself is either loaded from online sources are available in a subdirectory called `data` in the `data` sub-package.

The following examples are available:
* Census adult data set (three versions)
* CIFAR10 image data set
* Newsgroup data set
* Patient data set

## Census examples
Census examples are available in the sub-package `census`

More information about the census adult data set can be found here:

[https://archive.ics.uci.edu/ml/datasets/adult](https://archive.ics.uci.edu/ml/datasets/adult)

The objective for the presented models is to predict whether the income exceeds $50K/yr.

The census data set was augmented with random first- and lastnames for the purpose of privacy demonstration. A simple script to add names to the dataset can look like this:
```python
import censusname
from tqdm import tqdm

if __name__ == '__main__':
    lines, new_lines = [], []
    with open('adult.data', 'r') as inputfile:
        lines = inputfile.readlines()
    for line in tqdm(lines):
        new_lines.append('{}, {}'.format(censusname.generate(nameformat='{surname}, {given}'), line))
    with open('adult_with_names.csv', 'w') as outputfile:
        outputfile.writelines(new_lines)
```

The `census` example package contains three different examples:
1. UserModel and UserSource based on the (augmented) raw census data set.
2. A definition based on the already preprocessed data set.
3. A Bayesian model as an alternative to 1.

### Census raw
This example is placed in `census.raw`.

The `UserSource` provides a `read()` function that reads the adult CSV data and defines the features and a `preprocess()` function that is used to transform the data to a format that can be used by the neural network defined in `UserModel`.

The [run_demo.py](census/raw/run_demo.py) script provides a demo how to run this code locally. If you want to use it in a DQ0 project copy the `UserModel` class code and the `UserSource` code to the corresponding project directories or use the SDKs set_code functions.

Note that the `setup_data()` function in this example uses the data source's `preprocess()` function to both read and preprocess the data for later use in the model training.
Alternatively, the `preprocess()` function can serve as a data transformation step that is performed inside DQ0 as a data job. This job will produce a new data set that is connected to the original one and consists of the preprocessed (transformed) data.

### Census preprocessed
One such preprocessed data set can be found in the `preprocess` example: [census/preprocessed/data/data/adult_processed.csv](census/preprocessed/data/data/adult_processed.csv).

The second census example uses this data set to train the model.

The `UserModel` is almost identical to the raw example, the only difference being the call to the data source's `read()` function instead of `preprocess()` as this time, the CSV data already has the correct format.

The `DataSource` definition is accordingly very lean in this example. The class is derived from `CSVSource` to read the CSV data; no additional funcationality is needed.

### Census bayesian
This last census example provides an alternative to the neural network based income prediction. `UserSource` code, including read and preprocess is similar, only the model definition of `UserModel` has changed.

## CIFAR10
This example is placed in `cifar`.

This example demonstrates the use of DQ0 with image data. The presented data source is an implementation for the CIFAR10 data set.

More information on CIFAR10 can be found here: [https://www.cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html)

The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images.

The included model definition forms a convolutional neural network based on either this paper [https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py](https://github.com/AhmedSalem2/ML-Leaks/blob/master/classifier.py) or this Tensorflow tutorial [https://www.tensorflow.org/tutorials/images/cnn](https://www.tensorflow.org/tutorials/images/cnn).

## Newsgroups
This example is placed in `newsgroups`.

This is a text classification example known from the Scikit-learn API: [https://scikit-learn.org/stable/datasets/index.html#the-20-newsgroups-text-dataset](https://scikit-learn.org/stable/datasets/index.html#the-20-newsgroups-text-dataset).

From the scikit-learn documentation: The 20 newsgroups dataset comprises around 18000 newsgroups posts on 20 topics split in two subsets: one for training (or development) and the other one for testing (or for performance evaluation). The split between the train and test set is based upon a messages posted before and after a specific date.

## Patient
This example is placed in `patient`.

Regression example with a data set from Synthea, an open-source patient population simulation made available by The MITRE Corporation: [https://synthea.mitre.org/downloads](https://synthea.mitre.org/downloads).

Target column is the birthdate of patients. Features used are general patient record information.