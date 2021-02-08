#! /usr/bin/python3

"""
Python script to import data based on ghg coordinates, without using Google
Colab, allowing us to preserve usage limits for AI training. 
"""

import ee
import os

from PIL import Image
from pprint import pprint 

from fyputil import fyp_constants as fc 
from fyputil import ee_constants as ec

ee.Authenticate()
ee.Initialize()
