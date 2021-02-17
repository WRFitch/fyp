#! /usr/bin/python3

"""
A command-line script to take the existing images in a given directory, and 
store copies in the following configurations:
horz flip
rotated 90 degrees clockwise * 3
Every valid non-duplicated combination of the above transforms

see fastai for other good transforms. 
"""

import os 
import PIL
import sys
from PIL import Image 
from PIL import ImageDraw

#def filepaths
r90 = "r90"
r180 = "r180"
r270 = "r270"
  
# ARG FORMAT IS DIR, THEN NOTHING
imgdir = sys.argv[1]

def dupeAndFlip(image, imgdir, filename):
  image.save(f"{imgdir}/normal/{filename}")
  flip = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
  flip.save(f"{imgdir}/hflip/{filename}")
  
for file in os.listdir(imgdir):
  try:
    filesplit = os.path.split(file)
    print(file)

    img = Image.open(file)
    r90 = img.transpose(PIL.Image.ROTATE_90)
    r180 = img.transpose(PIL.Image.ROTATE_180)
    r270 = img.transpose(PIL.Image.ROTATE_270)
    dupeAndFlip(img, f"{imgdir}/../orig", file)
    dupeAndFlip(r90, f"{imgdir}/../r90", file)
    dupeAndFlip(r180, f"{imgdir}/../r180", file)
    dupeAndFlip(r270, f"{imgdir}/../r270", file)
  except Exception:
    print("that ain't no image")
    print()
  
