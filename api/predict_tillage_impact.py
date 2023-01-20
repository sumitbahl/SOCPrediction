from sklearn.preprocessing import OrdinalEncoder
import pickle
import pandas as pd


class TillagePredictor:

    def __init__(self):
        self.encoder = pickle.load(open("saved_objects/tillage/tillage_encoder.pickle", "rb"))
        self.random_forest = pickle.load(open("saved_objects/tillage/tillage_random_forest.pickle", "rb"))

    def predict(self, current_tillage, selected_tillage, current_soc_or_toc, depth, norm):
        data = {
            "control": current_tillage,
            "rvUnits": "%",
            "controlValue": current_soc_or_toc,
            "treatment": selected_tillage,
            "sampleDepth": depth,
            "studyLength": 5,
            "startYear": 2023,
            "norm": norm
        }
        test_df = pd.DataFrame([data])
        print(test_df.head())
        to_encode = ["control", "treatment", "sampleDepth", "rvUnits"]
        test_df[to_encode] = self.encoder.transform(test_df[to_encode])

        return self.random_forest.predict(test_df)[0]


if __name__ == "__main__":
    tillage_predictor = TillagePredictor()
    print(tillage_predictor.predict(
        "Conventional tillage", "No tillage", "0-30 cm", 2))

# example
data = {
    # or Conventional tillage, Conservation tillage, Zonal tillage
    "control": "Conventional tillage",
    "rvUnits": "%",
    "controlValue": -5,
    "treatment": "No tillage",  # or conservation tillage or zonal tillage
    "sampleDepth": "0-30 cm",
    "studyLength": 50,
    "startYear": 2023,
    "norm": 2
}

test__ = pd.DataFrame([data])

# test__[to_encode] = encoder.transform(test__[to_encode])
