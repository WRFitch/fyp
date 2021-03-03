#==============================================================================
# GOOGLE EARTH ENGINE UTILITIES
#==============================================================================

import constants as c

import csv
import ee
import json
import os
import pandas as pd
import time

#TODO remove json import and just parse the string normally
#TODO import image from given coordinates, no csv parsing or nothin 

def exportTable(table, scale, folder="no_export_folder", desc="no_desc"):
  ee.batch.Export.table.toDrive(
    collection = table,
    description = desc,
    folder = folder,
    fileFormat = "CSV"
  ).start()

# Export one table of the given image, at the scale and dimensions specified.
def exportTableFromImage(image, polygon, scale, folder="no_export_folder", 
    desc="no_desc"):
  exportTable(sample(image, polygon, scale), scale, folder, desc)
  
# samples image into feature_collection. 
# TODO rename to be a getDATATYPE, once we know the datatype returned from this.
#      It's likely to be a FeatureCollection. 
def sample(img, region, scale):
  return img.sampleRegions(
      collection = region,
      geometries = True,
      scale = scale
  )

# Export one GeoTIFF image of the given image, at the scale and dimension 
# specified.
def exportGeotiff(image, polygon, scale, folder="no_export_folder", 
    desc="no_desc"):
  ee.batch.Export.image.toDrive(
    crs = 'EPSG:3857',
    description = desc,
    fileFormat = 'GeoTIFF',
    folder = folder,
    image = image,
    maxPixels = 10e9,
    region = polygon,
    scale = scale
  ).start()

# Gets a square kilometer with the given point object as the centroid. 
# TODO is this definitely a square kilometer? 
def getSqKmFromPoint(point):
  return getRangeFromPoint(point, 500)

def getRangeFromPoint(point, range):
  return point.buffer(range).bounds()

# Read in CSV from drive
# This method is bad, and I should feel bad 
def getImgsFromCsv(csv_path, img):
  with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    firstRow = True
  
    # The number of simultaneous exports can't go over 3 or 4 without taking a 
    # performance hit. 
    concurrent_exports = 3
    export_buffer = []

    for row in csv_reader:
      if firstRow:
        firstRow = False
        continue

      # coords are stored as [LONGITUDE, LATITUDE]
      coords = json.loads(row[2]).get("coordinates")
      polygon = getSqKmFromPoint(ee.Geometry.Point(coords))
      name = f"{coords[0]}_{coords[1]}"
      tifname = name + ".tif"

      # skip files that have already been exported. 
      if os.path.isfile(f"{c.png_dir}/{name}.png") or \
          os.path.isfile(f"{c.data_dir}/geotiff/{tifname}") or \
          os.path.isfile(f"{c.drive_path}{c.geotiff_dir}/{tifname}"):
        # TODO update to include variable log levels
        print(f"skipping  {name} - file already exists!")
        continue
        
      export_buffer.append(tifname)
      print(f"exporting {tifname}")
      exportGeotiff(img, polygon, 10, c.geotiff_dir, name)

      # Block until export buffer is smaller than the maximum allowed concurrent 
      # exports. 
      while len(export_buffer) >= concurrent_exports:
        time.sleep(5)
        # when the files stored in the export buffer are found in the filesystem, 
        # remove them.
        for filename in export_buffer:
          if os.path.isfile(f"{c.drive_path}{c.geotiff_dir}/{filename}"): 
            export_buffer.remove(filename)
            print(f"exported  {filename}")
  
  print(f"exported {csv_path}")

def getBigImgsFromDf(df, img):
  # limit concurrent exports to avoid performance hit
  concurrent_exports = 3
  export_buffer = []

  for _, row in df.iterrows():
    coords = (row.longitude, row.latitude)
    # Arbitrarily defining the pixels, this gives us 224px
    polygon = getRangeFromPoint(ee.Geometry.Point(coords), 700)
    name = f"{coords[0]}_{coords[1]}"
    tifname = name + ".tif"
    
    export_buffer.append(tifname)
    print(f"exporting {tifname}")
    exportGeotiff(img, polygon, 10, "big_geotiff", name)

    while len(export_buffer) >= concurrent_exports:
      time.sleep(10)
      # when the files stored in the export buffer are found in the drive,
      # remove them 
      for filename in export_buffer:
        if os.path.isfile(f"{c.local_drive}/big_geotiff/{filename}"): 
          export_buffer.remove(filename)
          print(f"exported  {filename}")