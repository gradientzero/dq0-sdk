# -*- coding: utf-8 -*-
"""Process Yaml Config

Process yaml file to instantiate a basic tensorflow 
neural network implementation using Keras.

TODO:
    * Complete example doc string 
    
Example:
    if __name__ == "__main__":
        yaml_path = 'your path'
        yaml_config = YamlConfig(yaml_path)

        model = MyAwesomeModel(yaml_config)
        model.setup_model()
        ...

:Authors:
    Craig Lincoln <cl@gradient0.com>
    

Copyright 2020, Gradient Zero
All rights reserved
"""

import yaml

import tensorflow as tf
from tensorflow import keras

class YamlConfig():
    """Yaml parser for tf.keras models

    SDK uses this to create NN models and
    other paramters, eg, optimizers, loss, model path
    """
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
        """Reads yaml file
        
        This function parses a yaml file to self.yaml_dict
        """
        with open(self.yaml_path, 'r') as yaml_file:
            self.yaml_dict=yaml.load(yaml_file, Loader=yaml.Loader) # turnsout SafeLoader doesnt recognise !!python/tuple
        return self.yaml_dict

    def save_yaml(self):
        """Save yaml dict to a yaml file"""
        with open(self.yaml_path, 'w') as yaml_file:
            yaml_file.write(self.yaml_dict)

    def model_from_yaml(self):
        """Create instance of tf.keras model from yaml

        This function returns a tf.keras model instance
        """
        self.read_yaml_file()
        model_dict = self.yaml_dict['Model']
        model_dict['class_name'] = 'Sequential'
        model_dict['config']['name'] = 'sequential'
        model_str = yaml.dump(model_dict)
        
        # TODO: add control of custom_objects
        model = tf.keras.models.model_from_yaml(model_str, custom_objects={})
        return model

    def optimizer_para_from_yaml(self):
        """Return parameters for dp_optimizer"""
        opt_para = self.yaml_dict['dp_optimizer parametes']
        return opt_para

    def loss_from_yaml(self):
        """returns instance of loss function"""
        loss = keras.losses.get(self.yaml_dict['LOSS']['class_name'])
        if len(self.yaml_dict['LOSS'].items()):
            loss_config = loss.get_config()
            for k,v in self.yaml_dict['LOSS'].items():
                if k in loss_config.keys():
                    loss_config[k] = v
        # print(loss_config)
        loss = loss.from_config(loss_config)
        return loss
        

