import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
from tensorflow_privacy.privacy.optimizers import dp_optimizer

custom_objects = {'KerasLayer': hub.KerasLayer,
                  'GradientDescentOptimizer': dp_optimizer.GradientDescentOptimizer} 

