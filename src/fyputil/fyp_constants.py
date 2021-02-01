drive_path = "/content/drive/MyDrive/"
export_dir = "img_export"
geotiff_dir = "geotiff_export"
data_dir = f"{drive_path}{export_dir}"
png_dir = f"{data_dir}/png"

CO_band = 'CO_column_number_density'
HCHO_band = 'tropospheric_HCHO_column_number_density'
NO2_band = 'tropospheric_NO2_column_number_density'
O3_band = 'O3_column_number_density'
SO2_band = 'SO2_column_number_density'
CH4_band = 'CH4_column_volume_mixing_ratio_dry_air'
ghg_bands = [CO_band, HCHO_band, NO2_band, O3_band, SO2_band, CH4_band]

lon = "longitude"
lat = "latitude"


