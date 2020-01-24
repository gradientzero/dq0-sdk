# -*- coding: utf-8 -*-
"""Process Yaml Config

Process yaml file to instantiate a basic tensorflow 
neural network implementation using Keras.

TODO:
    * Complete example doc string 
    
Example:
    class MyAwsomeModel(dq0.models.tf.NeuralNetwork):
        def init():
            self.learning_rate = 0.3

        def setup_data():
            # do something
            pass

        def setup_model():
            # freely deinfe the tf / keras model
            pass

    if __name__ == "__main__":
        myModel = MyAwsomeModel()
        myModel.setup_data()
        myModel.setup_model()
        # myModel.fit()
        myModel.fit_dp()
        myModel.save()


    ./dql-cli deploy-model --model-name

    ./dql-cli evalute-model --model-name
    return myModel.evalute()

    ./dql-cli model-predict --sdfsd
    return myModel.predict()

:Authors:
    Craig Lincoln <cl@gradient0.com>
    

Copyright 2020, Gradient Zero
All rights reserved
"""

import yaml

import tensorflow as tf
from tensorflow import keras

class YamlConfig():
    def __init__(self, 
                 yaml_path, 
                 yaml_dict=None):
        self.yaml_str = None
        self.yaml_path = yaml_path
        if yaml_dict is None:
            self.read_yaml_file()
        else:
            self.yaml_dict=yaml_dict   
        
    def read_yaml_file(self):
        with open(self.yaml_path, 'r') as yaml_file:
            self.yaml_dict=yaml.load(yaml_file, Loader=yaml.Loader) # turnsout SafeLoader doesnt recognise !!python/tuple
        return self.yaml_dict

    def save_yaml(self):
        with open(self.yaml_path, 'w') as yaml_file:
            yaml_file.write(self.yaml_dict)

    def model_from_yaml(self):
        self.read_yaml_file()
        model_dict = self.yaml_dict['Model']
        model_dict['class_name'] = 'Sequential'
        model_dict['config']['name'] = 'sequential'
        model_str = yaml.dump(model_dict)
        
        # TODO: add control of custom_objects
        model = tf.keras.models.model_from_yaml(model_str, custom_objects={})
        return model

    def optimizer_para_from_yaml(self):
        opt_para = self.yaml_dict['dp_optimizer parametes']
        return opt_para
        

