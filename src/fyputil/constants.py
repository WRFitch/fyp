#==============================================================================
# FYP Constants 
#==============================================================================

import os

drive_path = "/content/drive/MyDrive/"
local_drive = "/home/will/drive/"
# Hacky way of having automatic userspace changes for local import scripts. 
# It's not scalable, but it's ok for hacking around. 
if os.environ.get('USERNAME') == 'will':
  drive_path = local_drive

# define filepath utilities 
export_dir = "img_export"
geotiff_dir = "geotiff_export"
data_dir = f"{drive_path}{export_dir}"
png_dir = f"{data_dir}/png"
big_png_dir = f"{data_dir}/png_224"
demo_dir = f"{drive_path}/demo_export"
model_dir = f"{drive_path}/models"
model_name = "140321_add-normalisation_bs-128_trained-some-more"
ghg_csv = f"{data_dir}/ghgs.csv"

CO_band = 'CO_column_number_density'
HCHO_band = 'tropospheric_HCHO_column_number_density'
NO2_band = 'tropospheric_NO2_column_number_density'
O3_band = 'O3_column_number_density'
SO2_band = 'SO2_column_number_density'
CH4_band = 'CH4_column_volume_mixing_ratio_dry_air'
ghg_bands = [CO_band, HCHO_band, NO2_band, O3_band, SO2_band, CH4_band]

fomula_names = {
  CO_band: "Carbon Dioxide",
  HCHO_band: "Formaldehyde",
  NO2_band: "Nitrogen Dioxide",
  O3_band: "Ozone",
  SO2_band: "Silicon Dioxide",
  CH4_band: "Methane"
}

lon = "longitude"
lat = "latitude"

# Though this is coordinate data, it is included here so we don't always have 
# to import, authenticate, and initialize EE if we want to test something. 
brunel_coords = (-0.47278354461716354, 51.53325658151181)