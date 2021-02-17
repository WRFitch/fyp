#==============================================================================
# FYP UTILITIES
# TODO rename to filename utilities
#==============================================================================

import constants as c

import csv
import json
import os

import numpy as np 
import pandas as pd

# Currently no easy one-line import for host pc - considering this is only 
# running on jupyter, I don't think this matters. 
from osgeo import gdal

# get filename from filepath, remove file extension and split into longitude and
# latitude. 
def getCoords(img_path):
  #print(img_path)
  return list(map(float, img_path.split("/")[-1][0:-4].split("_")))

def getFilepath(coords):
  return f"{c.png_dir}/{coords[0]}_{coords[1]}.png"

def imgExported(coords):
  return os.path.isfile(getFilepath(coords))

# Get the row from the given dataframe at the given coordinates.
# We have to define rounded precision because floats suck. There should be a 
# better way of doing this...
def getValAt(coords, df, prec=10):
  return df.loc[(round(df["longitude"], prec) == round(coords[0], prec)) & \
                (round(df["latitude" ], prec) == round(coords[1], prec))]

# Extracts lat and long volumes from .geo param in csv. 
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
        # Could string parsing be made more efficient? 
        # This method only needs to run once per csv so optimisation isn't that 
        # important. 
        coords = json.loads(row[2]).get("coordinates")
        row.append(coords[0])
        row.append(coords[1])

      csv_writer.writerow(row)
  
  os.remove(csv_path)
  os.rename(csv_path + test_suffix, csv_path)

# removes old geoTIFF images or xml conversion artifacts from the given directory. 
def rmArtifact(artifact_path, rmTif = False, rmXml = False):
  if not os.path.isfile(artifact_path): 
    print(f"{artifact_path} does not exist")
    return
  if not (rmTif or rmXml): return
  
  extension = os.path.splitext(artifact_path)[1].lower()
  if (extension == ".tif" and rmTif) or \
      (extension == ".xml" and rmXml): 
    print(f"removing {artifact_path}")
    os.remove(artifact_path)

def rmConversionArtifacts(path, rmTif = False, rmXml = False):
  # No point checking all these files if we're not going to do anything 
  if not (rmTif or rmXml): return

  parent_path = os.path.join(c.drive_path, path)
  for root, dirs, files in os.walk(parent_path, topdown=True):
    for name in files:
      fullpath = os.path.join(root, name)
      rmArtifact(fullpath, rmTif, rmXml)

def geotiffToPng(tif_path, rm_artifacts = False):
  # Define rgb bands and file extension
  options_list = [
    '-ot Byte',
    '-of PNG',
    '-b 4',
    '-b 3',
    '-b 2',
    '-scale'
  ]
  options_string = " ".join(options_list)
  parent_path = os.path.join(c.drive_path, tif_path)

  # Recursively walk through all files (this has to be simpler)
  for root, _, files in os.walk(parent_path, topdown=False):
    for name in files:
      full_path = os.path.join(root, name)
      print(full_path)
      split_path = os.path.splitext(full_path)

      if split_path[1].lower() != ".tif": continue

      path = split_path[0]
      filename = path.split("/")[-1]
      if os.path.isfile(path + ".png") or \
          os.path.isfile(f"{c.png_dir}/{filename}.png"):
        print(f"A png file already exists for {full_path}")
        continue
      
      gdal.Translate(
        path + '.png',
        path + '.tif',
        options = options_string
      )
      print(f"Converted {filename} from GeoTIFF to PNG")
      if rm_artifacts: rmArtifact(full_path, True, True)

# Move files from src to dest if they have the correct extension
def moveFilesByExtension(src, dest, extension):
  parent_path = os.path.join(c.drive_path, src)
  print(parent_path)

  for root, _, files in os.walk(parent_path, topdown=True):
    for name in files:
      full_path = os.path.join(root, name)
      split_path = os.path.splitext(full_path)
      if split_path[1].lower() == extension:
        dest_path = full_path.replace(src, dest)
        os.rename(full_path, dest_path)

def normGhgDfProperly(ghg_df):
  for band in c.ghg_bands:
    max = ghg_df[band].max()
    min = ghg_df[band].min()
    ghg_df[band] = ghg_df[band].apply(lambda x: (x-min)/(max-min) * 100)
  return ghg_df

def deNormGhgPrediction(prediction, ghg_df):
  denormed = []
  idx = 0
  for band in c.ghg_bands:
    max = ghg_df[band].max()
    min = ghg_df[band].min()
    denormed.append(((prediction[idx]/100) * (max-min)) + min)
    idx += 1 
  return denormed

def getGhgs(img_path, df): 
  coords = getCoords(str(img_path))
  ghgs = getValAt(coords, df)
  concentrations = ghgs[c.ghg_bands]
  if len(concentrations) == 0 : return None 
  if None in concentrations: return None
  # There has to be a cleaner way to do this. Iterating through and then only getting the first line? really? 
  return [tuple(x) for x in concentrations.to_numpy()][0]

def getGhgsAsArr(img_path, df):
  return np.array(getGhgs(img_path, df))
  
# TODO add file indexing into one CSV with all our latlong exports.