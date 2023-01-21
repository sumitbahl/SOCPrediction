import pickle
import pandas as pd


class ContinuousCoverPredictor:

    def __init__(self):
        self.encoder = pickle.load(open(
            "saved_objects/continuous_cover/continuous_cover_encoder.pickle", "rb"))
        self.random_forest = pickle.load(
            open("saved_objects/continuous_cover/continuous_cover_random_forest.pickle", "rb"))

    def predict(self, croptype, fertilization, current_continuous_cover, future_continuous_cover, current_soc_or_toc, speciestype, numspecies, depth, norm):
        # fertilization can be Uniform or Variable
        # croptype can be Cereal, Vegetable, Bean, Tree, or Bare Soil
        # current continuous cover can be bare soil or monocrop
        # future continuous cover can be intercrop, monocrop, or alley crop
        
        if current_continuous_cover == future_continuous_cover:
            return 0
        
        data = {
            "rvUnits": "%",
            "controlValue": current_soc_or_toc,
            "sampleDepth": depth,
            "studyLength": 5,
            "startYear": 2023,
            "norm": norm,
            "fertilization": fertilization,
            "speciestype": speciestype,
            "numspecies": numspecies
        }

        for croptype_option in ["Cereal", "Vegetable", "Bean", "Tree", "Bare Soil"]:
            if croptype == croptype_option:
                data[croptype_option + "_croptype"] = 1
            else:
                data[croptype_option + "_croptype"] = 0

        current_continuous_cover_options = [
            'bare soil_control',
            'monocrop_control'
        ]

        future_continuous_cover_options = [
            'intercrop_treatment',
            'monocrop_treatment',
            'alley crop_treatment'
        ]

        for option in current_continuous_cover_options:
            data[option] = int(
                option.replace("_control", "") == current_continuous_cover)

        for option in future_continuous_cover_options:
            data[option] = int(
                option.replace("_treatment", "") == future_continuous_cover)

        test_df = pd.DataFrame([data])

        to_encode = ["rvUnits", "sampleDepth", "speciestype", "fertilization"]
        test_df[to_encode] = self.encoder.transform(test_df[to_encode])

        feature_cols_in_order = [
            "rvUnits",
            "startYear",
            "studyLength",
            "sampleDepth",
            "controlValue",
            "numspecies",
            "speciestype",
            "fertilization",
            'bare soil_control', 'monocrop_control', 'intercrop_treatment',
            'monocrop_treatment', 'alley crop_treatment', 'Tree_croptype',
            'Bean_croptype', 'Bare Soil_croptype', 'Vegetable_croptype',
            'Cereal_croptype'
        ]

        return self.random_forest.predict(test_df[feature_cols_in_order])[0]


if __name__ == "__main__":
    continuous_cover_predictor = ContinuousCoverPredictor()
    print(continuous_cover_predictor.predict("Cereal", "Uniform",
          "monocrop", "intercrop", 1, "Legume & Non-Legume", 2, "0-30 cm", 2))
