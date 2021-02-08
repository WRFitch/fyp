#==============================================================================
# Earth Engine Constants
# To use:
# pip install earthengine-api
# ee.Authenticate()
# ee.Initialize() 
#==============================================================================

import ee 

# Define collections for each dataset to be used 
s2 = ee.ImageCollection("COPERNICUS/S2_SR")
s5_CO = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO")
s5_HCHO = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
s5_NO2 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
s5_O3 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_O3")
s5_SO2 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2")
s5_CH4 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4")

fs2 = ee.FeatureCollection("COPERNICUS/S2_SR")
fs5_CO = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_CO")
fs5_HCHO = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
fs5_NO2 = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_NO2")
fs5_O3 = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_O3")
fs5_SO2 = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_SO2")
fs5_CH4 = ee.FeatureCollection("COPERNICUS/S5P/OFFL/L3_CH4")

start_date = '2020-01-01'
end_date = '2020-12-31'
vis_palette = ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']

# GOOGLE EARTH ENGINE POLYGON BOUNDARY OBJECTS
great_britain = ee.Geometry.Polygon(
        [[[-1.836112801004015, 59.808076330562756],
          [-8.779472176004015, 58.82140293049428],
          [-7.988456551004015, 55.71069203454839],
          [-11.196464363504015, 54.42753859549109],
          [-11.328300301004015, 50.967746003015044],
          [-9.526542488504015, 50.77361752815123],
          [-6.274589363504015, 51.81776248652293],
          [-5.395683113504015, 51.21615275310099],
          [-6.582206551004015, 49.56332371186494],
          [-3.110526863504015, 49.904165426606255],
          [1.240059073995985, 50.80139967619036],
          [2.426582511495985, 52.33095407387208],
          [1.767402823995985, 53.4183511305661],
          [0.5369340739959849, 53.44453305344514],
          [-1.616386238504015, 56.32474216074427],
          [-0.7814253010040151, 57.805828290000164]]])

london = ee.Geometry.Polygon(
        [[[-0.8034984064310513, 51.86893967293553],
          [-0.8034984064310513, 51.10101596040769],
          [0.4077442693501787, 51.10101596040769],
          [0.4077442693501787, 51.86893967293553]]])

uxbridge = ee.Geometry.Rectangle(
        [[-0.5585304622116949, 51.577993458567235],
         [-0.3951088313523199, 51.51009512268249]])

# Used to check scaling is a-ok
millennium_dome = ee.Geometry.Polygon(
        [[[0, 51.51],
          [0, 51.49],
          [0.02, 51.49],
          [0.02, 51.51]]])

greenwich = ee.Geometry.Polygon(
        [[[-0.0, 51.55],
          [-0.0, 51.45],
          [0.1, 51.45],
          [0.1, 51.55]]])

west_hemisphere = ee.Geometry.Polygon(
        [[[-177.32831443211026, 84.89714695160266],
          [-177.32831443211026, -84.77052832075908],
          [0, -84.77052832075908],
          [0, 84.89714695160266]]])

east_hemisphere = ee.Geometry.Polygon(
        [[[0, 84.89714695160266],
          [0, -84.77052832075908],
          [173.5310605678897, -84.77052832075908],
          [173.5310605678897, 84.89714695160266]]])

