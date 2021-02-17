#! /usr/bin/python3

"""
Python script to import data based on ghg coordinates, without using Google
Colab, allowing us to preserve usage limits for AI training. 

TODO this requires drive mounting the same way it works on colab
"""

import ee
import os

#from google.colab import drive
#from osgeo import gdal

import fyputil.constants as c
import fyputil.ee_constants as eec
import fyputil.ee_utils as eeutil
import fyputil.fyp_utils as fyputi

ee.Authenticate()
ee.Initialize()

