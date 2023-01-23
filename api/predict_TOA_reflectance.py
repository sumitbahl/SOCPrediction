import pickle
import ee
import spyndex
import pandas as pd
import sklearn
import lightgbm
import matplotlib.pyplot as plt
import matplotlib
import time


class SOCTOCPredictor:

    def __init__(self):
        ee.Initialize()
        matplotlib.use('TkAgg')
        self.dataset = 'LANDSAT/LC08/C02/T1_RT_TOA'
        self.l8 = ee.ImageCollection(self.dataset)
        self.SOCscaler = pickle.load(open("saved_objects/soc_toc_mapping/TOA_scaler.pickle", "rb"))
        self.SOClgbm = lightgbm.Booster(model_file='saved_objects/soc_toc_mapping/TOA_LGBM.txt')

        self.TOCscaler = pickle.load(open("saved_objects/soc_toc_mapping/TOC_TOA_scaler.pickle", "rb"))
        self.TOClgbm = lightgbm.Booster(model_file='saved_objects/soc_toc_mapping/TOC_TOA_LGBM.txt')

    def select(self, coords, year):
        geometry = ee.Geometry.Polygon(coords)
        img = ee.Image(
            self.l8.filterBounds(geometry)
                .filterDate(f'{year}-01-01',
                            f'{year}-12-31')
                .sort('CLOUD_COVER').first()
        )
        return img.clip(geometry).select(list(range(11)))

    def SFIM(self, img, pan):
        imgScale = img.projection().nominalScale()
        panScale = pan.projection().nominalScale()

        kernelWidth = imgScale.divide(panScale)
        kernel = ee.Kernel.square(radius=kernelWidth.divide(2))

        panSmooth = pan.reduceNeighborhood(
            reducer=ee.Reducer.mean(),
            kernel=kernel
        )

        img = img.resample("bicubic")
        sharp = img.multiply(pan).divide(panSmooth).reproject(pan.projection())
        return sharp

    def pan_sharpen(self, img, bands):
        # print(type(img))
        to_sharpen = img.select(bands)
        # Select the 15 m panchromatic band
        pan = img.select(["B8"])

        return self.SFIM(to_sharpen, pan).addBands(pan)

    def compute_indices(self, img):
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
            "L": 1,
            "g": 2.5, "C1": 6, "C2": 7.5
        }

        indices = ['AFRI1600', 'AFRI2100', 'ANDWI', 'AVI', 'AWEInsh', 'AWEIsh', 'BAI', 'BAIM', 'BCC', 'BI', 'BLFEI', 'BNDVI', 'BRBA', 'BaI', 'CIG', 'CSI', 'CSIT', 'CVI', 'DBI', 'DBSI', 'DSI', 'DSWI1', 'DSWI2', 'DSWI3', 'DSWI4', 'DSWI5', 'DVI', 'EBBI', 'EMBI', 'EVI', 'EVI2', 'ExG', 'ExGR', 'ExR', 'FCVI', 'GARI', 'GBNDVI', 'GCC', 'GEMI', 'GLI', 'GNDVI', 'GOSAVI', 'GRNDVI', 'GRVI', 'GSAVI', 'GVMI', 'IBI', 'IKAW', 'IPVI', 'LSWI', 'MBI', 'MCARI1', 'MCARI2', 'MGRVI', 'MIRBI', 'MLSWI26', 'MLSWI27', 'MNDVI', 'MNDWI', 'MNLI', 'MRBVI', 'MSAVI', 'MSI', 'MSR', 'MTVI1', 'MTVI2', 'MuWIR', 'NBAI', 'NBLI', 'NBR', 'NBR2', 'NBRSWIR', 'NBRT1', 'NBRT2',
                   'NBRT3', 'NBSIMS', 'NBUI', 'NDBI', 'NDBaI', 'NDDI', 'NDGlaI', 'NDII', 'NDISIb', 'NDISIg', 'NDISImndwi', 'NDISIndwi', 'NDISIr', 'NDMI', 'NDPonI', 'NDSI', 'NDSII', 'NDSWIR', 'NDSaII', 'NDTI', 'NDVI', 'NDVIMNDWI', 'NDVIT', 'NDWI', 'NDYI', 'NGRDI', 'NIRv', 'NLI', 'NMDI', 'NRFIg', 'NRFIr', 'NSDS', 'NSDSI1', 'NSDSI2', 'NSDSI3', 'NSTv1', 'NSTv2', 'NWI', 'NormG', 'NormNIR', 'NormR', 'OSAVI', 'PISI', 'RCC', 'RDVI', 'RGBVI', 'RGRI', 'RI', 'RI4XS', 'S3', 'SARVI', 'SAVI', 'SAVIT', 'SI', 'SIPI', 'SR', 'SR2', 'SWI', 'SWM', 'TDVI', 'TGI', 'TVI', 'TriVI', 'UI', 'VARI', 'VI6T', 'VIBI', 'VIG', 'VgNIRBI', 'VrNIRBI', 'WI1', 'WI2', 'WI2015', 'WRI']

        for x in range(0, len(indices), 2):
            try:
                img = img.addBands(spyndex.computeIndex(
                    [indices[x], indices[x + 1]], parameters))
            except Exception as e:
                pass

        meanDict = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=img.geometry(),
            scale=90,
            maxPixels=40e9
        )

        # mappedDictionary = meanDict.map(lambda key, val:  val if val is not None else 0)

        return meanDict

    def predict(self, coords, min_year):
        # Combine selecting area, pan-sharpening, illumination, topographic correction, and spectral indices
        # returns dictionary of features

        predictions_SOC = {}
        predictions_TOC = {}

        for year in range(min_year, 2023):
            img = self.select(coords, year)
            img = img.scaleAndOffset()

            img = self.pan_sharpen(img, ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B9", "B10", "B11"])
            indices = self.compute_indices(img)

            indices_dict = indices.getInfo()

            df = pd.DataFrame([indices_dict])

            df = df.fillna(0)
            df_SOC_scaled = self.SOCscaler.transform(df)
            df_TOC_scaled = self.TOCscaler.transform(df)
            predictions_SOC[year] = self.SOClgbm.predict(df_SOC_scaled)[0]
            predictions_TOC[year] = self.TOClgbm.predict(df_TOC_scaled)[0]

        return {
            'SOC' : predictions_SOC,
            'TOC' : predictions_TOC
        }

    def plot(self, predictions_dict, filename, label):
        predictions_dict_list = predictions_dict.items()
        x, y = zip(*predictions_dict_list)
        plt.plot(x, y, label = label)
        plt.title('Subsoil and Topsoil Organic Carbon Sequestration Progress')
        plt.xlabel('Year')
        plt.ylabel('% Organic Carbon')
        plt.legend(loc='best')
        ax = plt.gca()
        ax.set_ylim([max(ax.get_ylim()[0] - 2, 0), min(ax.get_ylim()[1] + 2, 100)]) 
        # plt.show() # opens Tkinter GUI
        plt.savefig(filename)


SOC_predictor = SOCTOCPredictor()

if __name__ == '__main__':
    coords = [
        [-73.1333333333761, -54.0],
        [-73.0, -54.0],
        [-73.0, -54.0083333333477],
        [-73.1333333333761, -54.0083333333477],
        [-73.1333333333761, -54.0]
    ]

    SOC_predictor.plot(SOC_predictor.predict([coords], 2014)['SOC'])
