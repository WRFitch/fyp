#==============================================================================
# AI UTILITIES
#==============================================================================

# Since this isn't in a jupyter notebook anymore, we have to keep track of 
# imports. Update to only include what we're actually using, which is currently
# just model.predict()
from fastai.vision.all import *
#from fastai.tabular.all import *

import constants as c
import fyp_utils as fyputil
import pandas as pd

# Wrapper for ensemble learner to combine CNN and tabular model into an easy-to
# -use object. Object is speculative, rework after preliminary implementation
"""
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
"""

# get average Root Mean Squared Error values for the given model 
def getModelRmse(model, ghg_df, modulus=1, err_df=None):
  # Return a RMSE value for each GHG in the model's predicted values. 
  if err_df == None:
    err_df = getErrs(model, ghg_df, modulus)

  rtnval = []
  for col in c.ghg_bands:
    rtnval.append( math.sqrt( err_df[col].apply(lambda x:x**2) .mean()))
  return rtnval

def getPreds(model, ghg_df, modulus=1):
  # Return a dataframe containing the model predictions from the given dataframe
  pred_df = pd.DataFrame(columns=c.ghg_bands)
  mod = 0
  for _, row in ghg_df.iterrows():
    coords = (row.longitude, row.latitude)
    if not fyputil.imgExported(coords): continue
    if mod % modulus == 0 :
      prediction = model.predict(fyputil.getFilepath(coords))[0]
      pred_df.loc[len(pred_df)] = list(coords) + list(prediction)
    mod += 1
  return pred_df

def getErrs(model, df, modulus=1, preds_df=None):
  # Return a dataframe containing the difference between each prediction and the original value
  if preds_df == None:
    preds_df = getPreds(model, df, modulus)
  return fyputil.getDiffs(preds_df, df)

