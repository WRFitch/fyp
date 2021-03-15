#==============================================================================
# FYP UTILITIES
#
# TODO refactor to include a saner data pipeline 
# TODO refactor to be only file utils - this is currently too general. 
#==============================================================================

import constants as c

import csv
import json
import os

import numpy as np 
import pandas as pd

# TODO Currently no easy one-line import for host pc 
from osgeo import gdal

# Extracts lat and long volumes from .geo param in csv. 
# TODO refactor to use pandas df joins, rather than csv iteration 
# TODO move to data_utils.py
def parseCsvCoords(csv_path):
  print(csv_path)
  test_suffix = "_parsing_coordinates.csv"
  
  with open(csv_path, 'r') as read_obj, \
      open(csv_path + test_suffix, 'w', newline='') as write_obj:
    csv_reader = csv.reader(read_obj, delimiter=",")
    csv_writer = csv.writer(write_obj, delimiter=",")

    firstRow = True
    for row in csv_reader:
      if firstRow: 
        # break early if this method has already been applied to the given csv. 
        if "longitude" in row: 
          print(f"{csv_path} has already been processed - exiting...")
          return 
        row.append("longitude")
        row.append("latitude")
        firstRow = False
      else:
        coords = json.loads(row[2]).get("coordinates")
        row.append(coords[0])
        row.append(coords[1])

      csv_writer.writerow(row)
  
  os.remove(csv_path)
  os.rename(csv_path + test_suffix, csv_path)

# TODO move to file_utils.py
# removes old geoTIFF images or xml conversion artifacts from the given directory. 
def rmArtifact(artifact_path, rmTif = False, rmXml = False):
  if not (rmTif or rmXml): return
  if not os.path.isfile(artifact_path): 
    print(f"{artifact_path} does not exist")
    return
  
  extension = os.path.splitext(artifact_path)[1].lower()
  if (extension == ".tif" and rmTif) or \
      (extension == ".xml" and rmXml): 
    print(f"removing {artifact_path}")
    os.remove(artifact_path)

# TODO move to file_utils.py
def rmConversionArtifacts(path, rmTif = False, rmXml = False):
  # No point checking all these files if we're not going to do anything 
  if not (rmTif or rmXml): return

  parent_path = os.path.join(c.drive_path, path)
  for root, _, files in os.walk(parent_path, topdown=True):
    for name in files:
      fullpath = os.path.join(root, name)
      rmArtifact(fullpath, rmTif, rmXml)

# TODO move to data_utils.py
def geotiffToPng(tif_path, png_path = c.png_dir, rm_artifacts = False):
  options_string = '-ot Byte -of PNG -b 4 -b 3 -b 2 -scale'
  parent_path = os.path.join(c.drive_path, tif_path)

  for root, _, files in os.walk(parent_path, topdown=False):
    for name in files:
      full_path = os.path.join(root, name)
      print(full_path)
      split_path = os.path.splitext(full_path)

      if split_path[1].lower() != ".tif": continue

      path = split_path[0]
      filename = path.split("/")[-1]
      if os.path.isfile(path + ".png") or \
          os.path.isfile(f"{png_path}/{filename}.png"):
        print(f"A png file already exists for {full_path}")
        continue
      
      gdal.Translate(
        path + '.png',
        path + '.tif',
        options = options_string
      )
      print(f"Converted {filename} from GeoTIFF to PNG")
      if rm_artifacts: rmArtifact(full_path, True, True)

# TODO move to file_utils.py
# Move files from src to dest if they have the correct extension
def moveFilesByExtension(src, dest, extension):
  parent_path = os.path.join(c.drive_path, src)

  for root, _, files in os.walk(parent_path, topdown=True):
    for name in files:
      full_path = os.path.join(root, name)
      split_path = os.path.splitext(full_path)
      if split_path[1].lower() == extension:
        dest_path = full_path.replace(src, dest)
        print(f"moving files from {full_path} to {dest_path}")
        os.rename(full_path, dest_path)

# Get image coordinates from filename
def getCoords(img_path):
  return list(map(float, img_path.split("/")[-1][0:-4].split("_")))

# Get filepath of a given image 
def getFilepath(coords):
  return f"{c.big_png_dir}/{coords[0]}_{coords[1]}.png"

# Determine whether image has been exported
# TODO currently very slow to fail - find a faster way of doing this. 
def imgExported(coords):
  return os.path.isfile(getFilepath(coords))

# Get the row from the given dataframe at the given coordinates.
# Rounded precision must be defined due to floating-point issues.
# It would be better if this returned a list, rather than a sliced dataframe.
def getValAt(coords, df, prec=10):
  return df.loc[(round(df[c.lon], prec) == round(coords[0], prec)) & \
                (round(df[c.lat], prec) == round(coords[1], prec))]

def normGhgDf(ghg_df):
  for band in c.ghg_bands:
    max = ghg_df[band].max()
    min = ghg_df[band].min()
    ghg_df[band] = ghg_df[band].apply(lambda x: (x-min)/(max-min) * 100)
  return ghg_df

# TODO included for legacy, remove asap 
def deNormGhgPrediction(prediction, ghg_df):
  return deNormPrediction(prediction, ghg_df)

# Denormalises predicted GHG values. 
def deNormPrediction(prediction, ghg_df):
  denormed = []
  idx = 0
  for band in c.ghg_bands:
    max = ghg_df[band].max()
    min = ghg_df[band].min()
    denormed.append(((prediction[idx]/100) * (max-min)) + min)
    idx += 1 
  return denormed

# Get GHG values from dataframe based on image coordinates as stored in the 
# given path. 
# TODO optimise - this method is slow and clunky 
def getGhgs(img_path, df): 
  coords = getCoords(str(img_path))
  ghgs = getValAt(coords, df)
  concentrations = ghgs[c.ghg_bands]
  if len(concentrations) == 0 : return None 
  if None in concentrations: return None
  # There has to be a cleaner way to do this 
  return [tuple(x) for x in concentrations.to_numpy()][0]

# TODO test this method
def getGhgsFaster(img_path, df):
  coords = getCoords(str(img_path))
  ghgs = getValAt(coords, df).squeeze()
  if ghgs.empty: return None
  if None in ghgs: return None
  return np.array(ghgs) # TODO parse this however needed

#getGhgs as numpy array 
def getGhgsAsArr(img_path, df):
  return np.array(getGhgs(img_path, df))

# Checks the image is in the dataframe and can therefore be used
def imgIsInDf(img_path, df):
  coords = getCoords(str(img_path))
  return not getValAt(coords, df).empty

# TODO move to file_utils.py
def rmBracketedDupe(dir): 
  count = 0
  for root, dir, files in os.walk(dir):
    for file in files:
      if "(" in file:
        print(f"{root}/{file}")
        os.remove(f"{root}/{file}")
        count += 1
  print(count)
  