#!/usr/bin/python3

"""
Python script to import data based on ghg coordinates, without using Google
Colab, allowing us to preserve usage limits for AI training. 
"""

import ee
import os
import pandas as pd 

#from osgeo import gdal

ee.Authenticate()
ee.Initialize()

# These imports need to occur after authenitcation and initialisation
import ee_constants as eec
import ee_utils as eeutil

csv_path = "/src/fyp/datasets/ghgs/ghgs.csv"
ghg_data = pd.read_csv(csv_path)

eeutil.getBigImgsFromDf(ghg_data, eec.s2_img)