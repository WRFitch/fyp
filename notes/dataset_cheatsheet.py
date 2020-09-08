#!/usr/env/python3

"""This is a script detailing how to download, manipulate and evaluate a simple 
dataset. This isn't actually run by my FYP, but is a mirror of the code in my 
jupyter test notebooks. Ignore any IDE warnings here, this should all run fine 
on colab. 

You'll need to install the following fastai packages:
!pip install -Uqq fastai
!pip install -Uqq fastcore
!pip install -Uqq fastscript
!pip install -Uqq fastgpu
!pip install -Uqq fastai2
!pip install -Uqq fastbook
"""

from fastai2.vision.all import *
#Sometimes you need to remove the 2. This library can be temperamental.
#from fastai.vision.all import *

path = untar_data(URLs.PETS)/'images'

def is_cat(x): 
  return x[0].isupper() 

dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path), valid_pct=0.2, seed=42,
    label_func=is_cat, item_tfms=Resize(224))

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(2)