# Background

Carbon dioxide (CO2) is the most commonly produced greenhouse gas and is a major contributor to climate change. Carbon dioxide is removed, or sequestered, from the atmosphere when it is absorbed by plants as part of the biological carbon cycle, and it can be stored as soil organic carbon (SOC). SOC sequestration is beneficial in fighting climate change, but it is also crucial to soil health, fertility, and ecosystem services. Regenerative Agriculture practices may be a solution to sequestering large amounts of CO2.

There is a need for an efficient, accurate, and inexpensive method of quantifying the amount of SOC at any given location. Current methods have drawbacks. For example, dry combustion with automated analyzers is expensive and involves pretreatment with acid, which may destroy organic matter.

In this project, machine learning was applied to analyze multispectral remote sensing data from Landsat 8 to determine the amount of SOC at any given location. Machine learning was also applied to predict the impact of certain regenerative practices on future SOC levels. The models were deployed via a mobile app. 

# Data
3 datasets were used — the Harmonized World Soil Database (HWSD), Landsat 8 surface reflectance, and Landsat 8 top-of-atmosphere reflectance. Data processing took a while, so I published a [processed dataset on Kaggle](https://www.kaggle.com/datasets/reymaster/hwsd-landsat-processed), free to use. 

# Files/Directories
* `api` contains all the code used for deploying the models. The Flask Python library is used.
* `create_dataset` contains the code used for creating and sharing the processed dataset.
* `feature_extraction` contains the code for feature extraction
* `models` contains all the code for the machine learning models created
* The `.js` files in this directory contain all the code used in the Google Earth Engine for processing Landsat data.

Each of the directories mentioned above contains information on how to run the code found in that directory.

# Install Python libraries
Run the following command:
```
pip install -r requirements.txt
```