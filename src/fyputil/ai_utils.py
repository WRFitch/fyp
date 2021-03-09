#==============================================================================
# AI UTILITIES
#==============================================================================

from fastai.vision.all import *
from fastai.tabular.all import *

import pandas as pd

def test_model(model):
  print(model)

class EnsembleModel:
  cnnModel = None
  tabModel = None

  def __init__(self): self.init()

  def init(self, cnnModel=None, tabModel=None, dl=None, df=None):
    if cnnModel != None:
      self.cnnModel = cnnModel
    else: 
      self.cnnModel = cnn_learner(
        dl, 
        resnet152, 
        y_range=(0, 100),  
        metrics=rmse
      ).to_fp16()

    if tabModel != None:
      self.tabModel = tabModel
    else:
      tabModel = tabular_learner(df)

  def fit(self): self.tabModel.fit()
