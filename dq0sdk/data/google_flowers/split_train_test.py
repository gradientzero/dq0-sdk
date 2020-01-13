import os
import numpy as np
from random import sample

np.random.seed(1)

root_dir=os.getcwd()
train_data_dir = os.path.join(root_dir,'dq0sdk/data/google_flowers/flower_photos/train')

path_test = os.path.join(*[os.path.split(train_data_dir)[0],'test'])
if not os.path.exists(path_test):
  os.mkdir(path_test)
  for subdir in os.listdir(train_data_dir):
    if subdir not in ['LICENSE.txt']:
      path_test_name = os.path.join(*[os.path.split(train_data_dir)[0],'test',subdir])
      path_origin = os.path.join(train_data_dir,subdir)
      print(path_origin)
      if not os.path.exists(path_test_name):
        os.mkdir(path_test_name)
      files_to_move=sample(os.listdir(path_origin),32*5)
      for f in files_to_move:
        os.rename(os.path.join(path_origin,f), os.path.join(path_test_name,f))