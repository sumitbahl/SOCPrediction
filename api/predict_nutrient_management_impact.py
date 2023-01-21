import pickle
import pandas as pd


class NutrientManagementPredictor:

    def __init__(self):
        self.encoder = pickle.load(open(
            "saved_objects/nutrient_management/nutrient_management_encoder.pickle", "rb"))
        self.random_forest = pickle.load(
            open("saved_objects/nutrient_management/nutrient_management_random_forest.pickle", "rb"))

    def predict(self, croptype, current_fertilizer, future_fertilizer, current_soc_or_toc, depth, norm):
        # croptype can be Cereal, Vegetable, Bean, or Tree
        
        if current_fertilizer == future_fertilizer:
            return 0

        new_croptype = ""
        if croptype in ["Bean", "Tree"]:
            new_croptype = '["Cereal", "Bean", "Tree"]'
        elif croptype == "Cereal":
            new_croptype = '["Cereal"]'
        else:
            new_croptype = '["Vegetable"]'

        data = {
            "rvUnits": "%",
            "controlValue": current_soc_or_toc,
            "sampleDepth": depth,
            "studyLength": 5,
            "startYear": 2023,
            "norm": norm,
            "croptype": str(new_croptype)
        }

        current_fertilizers_options = [
            'Unspecified Mineral Fertilizer_control',
            'Potassium Mineral Fertilizer_control',
            'Nitrogen Mineral Fertilizer_control', 'Unamended_control',
            'Incinerated Organics_control', 'Green Manure_control',
            'Animal Manure_control', 'Phosphorus Mineral Fertilizer_control',
            'Legume Intercrop_control'
        ]

        future_fertilizers_options = [
            'Unspecified Mineral Fertilizer_treatment',
            'Legume Intercrop_treatment', 'Potassium Mineral Fertilizer_treatment',
            'Nitrogen Mineral Fertilizer_treatment', 'Animal Manure_treatment',
            'Incinerated Organics_treatment', 'Green Manure_treatment',
            'Phosphorus Mineral Fertilizer_treatment'
        ]

        for option in current_fertilizers_options:
            data[option] = int(
                option.replace("_control", "") == current_fertilizer)

        for option in future_fertilizers_options:
            data[option] = int(
                option.replace("_treatment", "") == future_fertilizer)

        test_df = pd.DataFrame([data])

        to_encode = ["rvUnits", "sampleDepth", "croptype"]
        test_df[to_encode] = self.encoder.transform(test_df[to_encode])

        feature_cols_in_order = [
            "rvUnits",
            "startYear",
            "studyLength",
            "sampleDepth",
            "controlValue",
            "norm",
            "croptype",
            'Unspecified Mineral Fertilizer_control', 'Legume Intercrop_control',
            'Potassium Mineral Fertilizer_control',
            'Nitrogen Mineral Fertilizer_control', 'Unamended_control',
            'Incinerated Organics_control', 'Green Manure_control',
            'Animal Manure_control', 'Phosphorus Mineral Fertilizer_control',
            'Unspecified Mineral Fertilizer_treatment',
            'Legume Intercrop_treatment', 'Potassium Mineral Fertilizer_treatment',
            'Nitrogen Mineral Fertilizer_treatment', 'Animal Manure_treatment',
            'Incinerated Organics_treatment', 'Green Manure_treatment',
            'Phosphorus Mineral Fertilizer_treatment'
        ]

        return self.random_forest.predict(test_df[feature_cols_in_order])[0]


if __name__ == "__main__":
    nutrient_managment_predictor = NutrientManagementPredictor()
    print(nutrient_managment_predictor.predict(
        "Cereal", "Unamended", "Animal Manure", 1, "0-30 cm", 2))
