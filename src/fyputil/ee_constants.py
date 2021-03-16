#==============================================================================
# Earth Engine Constants
#
# To use:
# pip install earthengine-api
# ee.Authenticate()
# ee.Initialize() 
#==============================================================================

import constants as c
import ee 
import folium

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


# Could the start and end dates be shifted or focused on one area, so emissions can be monitored across the seasons? 
# Would that even be useful? 
start_date = '2020-01-01'
end_date = '2020-12-31'
vis_palette = ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']

# polygon boundary object library - separate import? 
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

south_east =  ee.Geometry.Polygon(
        [[[-2.3050928044997576, 51.93002845408979],
          [-2.3050928044997576, 50.6417844886827],
          [1.4742040705002424, 50.6417844886827],
          [1.4742040705002424, 51.93002845408979]]])

# Define ImageCollection for each GHG 

# TODO analyse whether these min/max values are valid, recalibrate for highest 
#      variance where necessary. Separate values may be necessary for different
#      samples - for example, the perfect calibration for the UK won't work on 
#      the rest of the world. 
# TODO analyse whether it makes sense to analyse these on a highly localised level

# pre-filter function to remove clouds from satellite imagery - we can add them
# back in as data points from sentinel 5 if necessary
def maskS2clouds(image) :
  qa = image.select('QA60')

  # Bits 10 and 11 are clouds and cirrus, respectively.
  cloud_bitmask = 1 << 10
  cirrus_bitmask = 1 << 11

  # Both flags should be set to zero, indicating clear conditions.
  mask = qa.bitwiseAnd(cloud_bitmask).eq(0).And( \
         qa.bitwiseAnd(cirrus_bitmask).eq(0))

  return image.updateMask(mask).divide(10000)

# High-resolution satellite photograph 
s2_img = s2.filterDate(start_date, end_date) \
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
           .filterBounds(great_britain) \
           .map(maskS2clouds).median()

CO_img = s5_CO.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.CO_band).mean()

HCHO_img = s5_HCHO.filterDate(start_date, end_date) \
                  .filterBounds(great_britain) \
                  .select(c.HCHO_band).mean()

NO2_img = s5_NO2.filterDate(start_date, end_date) \
                .filterBounds(great_britain) \
                .select(c.NO2_band).mean()

O3_img = s5_O3.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.O3_band).mean()

SO2_img = s5_SO2.filterDate(start_date, end_date) \
                .filterBounds(great_britain) \
                .select(c.SO2_band).mean()

CH4_img = s5_CH4.filterDate(start_date, end_date) \
                .filterBounds(great_britain) \
                .select(c.CH4_band).mean()

ghg_imgs = [CO_img, HCHO_img, NO2_img, O3_img, SO2_img, CH4_img]

# Define IDs for each GHG
# Minmax scale is a bit off - recalibrate for my datasets to improve 
# visualisation
s2_id = s2_img.getMapId({'bands': ['B4', 'B3', 'B2'], \
                        'min': 0, \
                        'max': 0.3})

CO_id = CO_img.getMapId( \
    {'palette': vis_palette, \
    'min': 0, \
    'max': 0.05})

HCHO_id = HCHO_img.getMapId( \
    {'palette': vis_palette, \
    'min': 0.0, \
    'max': 0.0003})

NO2_id = NO2_img.getMapId( \
    {'palette': vis_palette, \
    'min': 0.0, \
    'max': 0.0002})

O3_id = O3_img.getMapId( \
    {'palette': vis_palette, \
    'min': 0.12, \
    'max': 0.15})

SO2_id = SO2_img.getMapId( \
    {'palette': vis_palette, \
    'min': 0.0, \
    'max': 0.0005})

CH4_id = CH4_img.getMapId( \
    {'palette': vis_palette, \
    'min': 1750, \
    'max': 1900})

ghg_ids = [CO_id, HCHO_id, NO2_id, O3_id, SO2_id, CH4_id]


# Define FeatureCollections for each GHG 
CO_fc = fs5_CO.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.CO_band)

HCHO_fc = fs5_HCHO.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.HCHO_band)

NO2_fc = fs5_NO2.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.NO2_band)

O3_fc = fs5_O3.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.O3_band)

SO2_fc = fs5_SO2.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.SO2_band)
  
CH4_fc = fs5_CH4.filterDate(start_date, end_date) \
              .filterBounds(great_britain) \
              .select(c.CH4_band)

ghg_fcs = [CO_fc, HCHO_fc, NO2_fc, O3_fc, SO2_fc, CH4_fc]

# Visualise data on a Folium map 
map_attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>'
layerOpacity = 0.5

map = folium.Map(
    location = [51.5, 0.1], 
    prefer_canvas = True)

folium.TileLayer(
    tiles = s2_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'satellite photography median composite '
  ).add_to(map)

folium.TileLayer(
    tiles = CO_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Carbon Monoxide',
    opacity = layerOpacity,
    show = False
  ).add_to(map)

folium.TileLayer(
    tiles = HCHO_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Formaldehyde',
    opacity = layerOpacity,
    show = False
  ).add_to(map)

folium.TileLayer(
    tiles = NO2_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Nitrogen Dioxide',
    opacity = layerOpacity,
    show = False
  ).add_to(map)

folium.TileLayer(
    tiles = O3_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Ozone',
    opacity = layerOpacity,
    show = False
  ).add_to(map)

folium.TileLayer(
    tiles = SO2_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Sulphur Dioxide',
    opacity = layerOpacity,
    show = False
  ).add_to(map)

folium.TileLayer(
    tiles = CH4_id['tile_fetcher'].url_format,
    attr = map_attr,
    overlay = True,
    name = 'Methane',
    opacity = layerOpacity,
    show = False
  ).add_to(map)
  
map.add_child(folium.LayerControl())