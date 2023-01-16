import pickle
import ee
import spyndex
import pandas as pd
import sklearn
import lightgbm


# already authenticated
# ee.Authenticate

ee.Initialize()

def select(long1, lat1, long2, lat2, year):
	rectangle = ee.Geometry.Rectangle([long1, lat1, long2, lat2])

	dataset = 'LANDSAT/LC08/C01/T1_TOA'

	l8 = ee.ImageCollection(dataset)

	img = ee.Image(
		l8.filterBounds(rectangle)
			.filterDate(f'{year}-01-01',
				f'{year}-12-31')
			.sort('CLOUD_COVER').first()
	)
	return img.clip(rectangle).select(list(range(11)))


def SFIM(img, pan):
	imgScale = img.projection().nominalScale()
	panScale = pan.projection().nominalScale()

	kernelWidth = imgScale.divide(panScale)
	kernel = ee.Kernel.square(radius = kernelWidth.divide(2))

	panSmooth = pan.reduceNeighborhood(
	reducer = ee.Reducer.mean(),
	kernel = kernel
	)

	img = img.resample("bicubic")
	sharp = img.multiply(pan).divide(panSmooth).reproject(pan.projection())
	return sharp

def pan_sharpen (img, bands):
	# print(type(img))
	to_sharpen = img.select(bands);
	# Select the 15 m panchromatic band
	pan = img.select(["B8"]);

	return SFIM(to_sharpen, pan).addBands(pan)

def compute_indices (img):
	dataset = 'LANDSAT/LC08/C01/T1_TOA'

	parameters = {
		"A": img.select("B1"),
		"B": img.select("B2"),
		"G": img.select("B3"),
		"R": img.select("B4"),
		"N": img.select("B5"),
		"S1": img.select("B6"),
		"S2": img.select("B7"),
		"T1": img.select("B10"),
		"T2": img.select("B11"),
		"L" : 1, 
		"g" : 2.5, "C1" : 6, "C2" : 7.5
	}

	indices = ['AFRI1600','AFRI2100','ANDWI','AVI','AWEInsh','AWEIsh','BAI','BAIM','BCC','BI','BLFEI','BNDVI','BRBA','BaI','CIG','CSI','CSIT','CVI','DBI','DBSI','DSI','DSWI1','DSWI2','DSWI3','DSWI4','DSWI5','DVI','EBBI','EMBI','EVI','EVI2','ExG','ExGR','ExR','FCVI','GARI','GBNDVI','GCC','GEMI','GLI','GNDVI','GOSAVI','GRNDVI','GRVI','GSAVI','GVMI','IBI','IKAW','IPVI','LSWI','MBI','MCARI1','MCARI2','MGRVI','MIRBI','MLSWI26','MLSWI27','MNDVI','MNDWI','MNLI','MRBVI','MSAVI','MSI','MSR','MTVI1','MTVI2','MuWIR','NBAI','NBLI','NBR','NBR2','NBRSWIR','NBRT1','NBRT2','NBRT3','NBSIMS','NBUI','NDBI','NDBaI','NDDI','NDGlaI','NDII','NDISIb','NDISIg','NDISImndwi','NDISIndwi','NDISIr','NDMI','NDPonI','NDSI','NDSII','NDSWIR','NDSaII','NDTI','NDVI','NDVIMNDWI','NDVIT','NDWI','NDYI','NGRDI','NIRv','NLI','NMDI','NRFIg','NRFIr','NSDS','NSDSI1','NSDSI2','NSDSI3','NSTv1','NSTv2','NWI','NormG','NormNIR','NormR','OSAVI','PISI','RCC','RDVI','RGBVI','RGRI','RI','RI4XS','S3','SARVI','SAVI','SAVIT','SI','SIPI','SR','SR2','SWI','SWM','TDVI','TGI','TVI','TriVI','UI','VARI','VI6T','VIBI','VIG','VgNIRBI','VrNIRBI','WI1','WI2','WI2015','WRI']
	

	for x in range(0, len(indices), 2):
		try:
			img = img.addBands(spyndex.computeIndex([indices[x], indices[x + 1]], parameters))
		except Exception as e:
			pass

	meanDict = img.reduceRegion(
		reducer= ee.Reducer.mean(),
		geometry= img.geometry(),
		scale= 90,
		maxPixels= 40e9
	)

	# mappedDictionary = meanDict.map(lambda key, val:  val if val is not None else 0)

	return meanDict

def predict(long1, lat1, long2, lat2):
	# Combine selecting area, pan-sharpening, illumination, topographic correction, and spectral indices
	# returns dictionary of features

	scaler = pickle.load(open("api/TOA_scaler.pickle", "rb"))
	lgbm = lightgbm.Booster(model_file = 'api/TOA_LGBM.txt')

	predictions = []

	for year in range(2014, 2022): 
		img = select(long1, lat1, long2, lat2, year)
		img = img.scaleAndOffset()

		img = pan_sharpen(img, ["B1", "B2", "B3", "B4", "B5", "B6", "B7","B9", "B10", "B11"])
		indices = compute_indices(img);

		indices_dict = indices.getInfo()

		df = pd.DataFrame([indices_dict])

		df = df.fillna(0)
		df_scaled = scaler.transform(df)

		predictions.append({year : lgbm.predict(df_scaled)[0]})
		print(predictions[-1])


	return predictions
	

print(predict(-73.	, -54.0083333333477, -73.1333333333761, -54.0))