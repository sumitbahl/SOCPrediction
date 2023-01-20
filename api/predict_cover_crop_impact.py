import pickle
import pandas as pd


class CoverCropPredictor:

    def __init__(self):
        self.encoder = pickle.load(open("saved_objects/cover_crops/cover_crop_encoder.pickle", "rb"))
        self.random_forest = pickle.load(open("saved_objects/cover_crops/cover_crop_random_forest.pickle", "rb"))

    def predict(self, type_of_species, number_of_species, current_soc_or_toc, depth, norm):
        # type of species can be "Non-legume" or "Rotation of Cover Crops"
        # number of species can be "Single species"
        data = {
            "rvUnits": "%",
            "controlValue": current_soc_or_toc,
            "Type of Species": type_of_species,
            "Number of Species": number_of_species,
            "sampleDepth": depth,
            "studyLength": 5,
            "startYear": 2023,
            "norm": norm
        }
        
        test_df = pd.DataFrame([data])
        to_encode = ["Type of Species", "Number of Species", "sampleDepth", "rvUnits"]
        test_df[to_encode] = self.encoder.transform(test_df[to_encode])

        return self.random_forest.predict(test_df)[0]


if __name__ == "__main__":
    tillage_predictor = CoverCropPredictor()
    print(tillage_predictor.predict(
        "Non-legume", "Single species", 1, "0-30 cm", 2))
