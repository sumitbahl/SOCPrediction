import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

def select(long1, lat1, long2, lat2):
    rectangle = ee.Geometry.Rectangle([long1, lat1, long2, lat2])

    dataset = 'LANDSAT/LC08/C02/T1_RT_TOA'

    l8 = ee.ImageCollection(dataset)

    img = ee.Image(
        l8.filterBounds(rectangle)
            .filterDate('2015-01-01',
                '2015-12-31')
            .sort('CLOUD_COVER').first()
    )
    return img.clip(rectangle).select(list(range(11))), rectangle


"""
run these commands, you must also get a Kaggle API key

!pip install -q kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d reymaster/hwsd-landsat-processed

! unzip "hwsd-landsat-processed.zip" -d latdata
"""

import pandas as pd

latdata = pd.read_csv('latdata/latdata/latdata.csv')
latdata.shape

latdata = latdata.drop_duplicates(subset=['MU_GLOBAL']).to_numpy()

import json
from collections import defaultdict


def do_thousand_images():
    f = open("/content/drive/MyDrive/SOC/counts_per_mu_global.json")
    counts_per_mu_global = defaultdict(lambda : 0, json.load(f))

    uploaded_image_count = int(open("/content/drive/MyDrive/SOC/images_uploaded_count").read())

    tasks = []
    for i in range(uploaded_image_count, uploaded_image_count + 1000):
        mu_global = str(int(latdata[i][0]))
        long1 = latdata[i][1]
        long2 = latdata[i][2]
        lat1 = latdata[i][3]
        lat2 = latdata[i][4]
        
        img, region = select(long1, lat1, long2, lat2)
        
        task = ee.batch.Export.image.toDrive(image=img,
                                        description='',
                                        scale=30,
                                        region=region,
                                        fileNamePrefix = mu_global,
                                        crs='EPSG:4326',
                                        fileFormat='GeoTIFF', folder= "geotiff_images")
        task.start()
        tasks.append(task)
        uploaded_image_count
        print(i)

        uploaded_image_count += 1
        counts_per_mu_global[mu_global] += 1

        with open('/content/drive/MyDrive/SOC/images_uploaded_count', 'w') as f:
            f.write(str(uploaded_image_count))

        with open('/content/drive/MyDrive/SOC/counts_per_mu_global.json', 'w') as f:
            json.dump(dict(counts_per_mu_global), f)

import time

for i in range(100):
    do_thousand_images()
    time.sleep(400)
