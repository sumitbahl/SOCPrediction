# Processed Dataset

Using the code in this directory (`/create_dataset`), a Kaggle dataset was created and can be found [here](https://www.kaggle.com/datasets/reymaster/hwsd-landsat-processed).

# How to process Harmonized World Soil Database (HWSD)
The processed data can be found on Kaggle, so it is not necessary to run the code in this directory. However, if you want to run it, below are the instructions:

1. Run `install_packages.R`
2. Go to this link: https://www.fao.org/soils-portal/soil-survey/soil-maps-and-databases/harmonized-world-soil-database-v12/en/ 
3. Click "HWSD Raster" and "Download database (.mdb)"
4. Update `HWSD.r` to the correct directory of the raster file. Make sure all three files (`hwsd.bil`, `hwsd.blw`, `hwsd.hdr`) are in the same directory.
5. Update the file paths in `Call_R_Scripts.ipynb` and run the notebook.

# How to link HWSD to Landsat
The processed data can be found on Kaggle, so it is not necessary to run the code in this directory. However, if you want to run it, below are the instructions:
1. Follow the instructions [here](https://developers.google.com/earth-engine/guides/python_install) to install the Google Earth Engine Python API
2. Create a Kaggle account and go to https://www.kaggle.com/account. Download an API token by clicking “Create New API Token” and move it to your root directory.
3. Run the following commands to use the Kaggle dataset. Alternatively, if you ran the programs to process HWSD, you can use the generated CSV files instead of the CSV files from the Kaggle dataset.

```text
!pip install -q kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d reymaster/hwsd-landsat-processed

! unzip "hwsd-landsat-processed.zip" -d latdata
```
4. Update the file paths in `google_earth_engine.py` and run.