import ast

from flask import Flask, jsonify, request, send_file
from predict_continuous_cover_impact import ContinuousCoverPredictor
from predict_cover_crop_impact import CoverCropPredictor
from predict_nutrient_management_impact import NutrientManagementPredictor
from predict_tillage_impact import TillagePredictor
from predict_TOA_reflectance import SOCTOCPredictor

app = Flask(__name__)

soc_toc_predictor = SOCTOCPredictor()
tillage_predictor = TillagePredictor()
cover_crop_predictor = CoverCropPredictor()
nutrient_managment_predictor = NutrientManagementPredictor()
continuous_cover_predictor = ContinuousCoverPredictor()

@app.route('/get_data')
def get_data():
    coords = ast.literal_eval(request.args.get('coords'))
    year = int(request.args.get('yearFrom'))
    # soc_predictor.predict(-73., -54.0083333333477, -73.1333333333761, -54.0, 2014)

    data = soc_toc_predictor.predict(coords, year)

    filename = f'img/{str(coords)}{year}.png'
    soc_toc_predictor.plot(data['SOC'], filename,
                           label="Subsoil Organic Carbon")
    soc_toc_predictor.plot(data['TOC'], filename,
                           label="Topsoil Organic Carbon")

    return jsonify(data)


@app.route('/get_plot')
def get_plot():
    coords = ast.literal_eval(request.args.get('coords'))
    year = int(request.args.get('yearFrom'))
    filename = f'img/{str(coords)}{year}.png'
    return send_file(filename, mimetype='image/gif')


@app.route('/tillage_impact')
def tillage_impact():
    coords = ast.literal_eval(request.args.get('coords'))
    current_tillage = request.args.get('currentTillage')
    selected_tillage = request.args.get('futureTillage')

    year_from = 2021
    soc_toc_predictions = soc_toc_predictor.predict(coords, year_from)

    current_soc = soc_toc_predictions['SOC'][year_from]
    current_toc = soc_toc_predictions['TOC'][year_from]

    data = {}
    data['percent_increase'] = tillage_predictor.predict(
        current_tillage=current_tillage,
        selected_tillage=selected_tillage,
        current_soc_or_toc=current_soc,
        depth="0-30 cm",
        norm=2
    )

    return jsonify(data)

@app.route('/cover_crop_impact')
def cover_crop_impact():
    coords = ast.literal_eval(request.args.get('coords'))
    type_of_species = request.args.get('typeOfSpecies')
    number_of_species = request.args.get('numberOfSpecies')

    year_from = 2021
    soc_toc_predictions = soc_toc_predictor.predict(coords, year_from)

    current_soc = soc_toc_predictions['SOC'][year_from]
    current_toc = soc_toc_predictions['TOC'][year_from]

    data = {}
    data['percent_increase'] = cover_crop_predictor.predict(
        type_of_species=type_of_species,
        number_of_species=number_of_species,
        current_soc_or_toc=current_soc,
        depth="0-30 cm",
        norm=2
    )

    return jsonify(data)

@app.route('/nutrient_management_impact')
def nutrient_management_impact():
    coords = ast.literal_eval(request.args.get('coords'))
    crop_type = request.args.get('croptype')
    current_fertilizer = request.args.get('currentFertilizer')
    future_fertilizer = request.args.get('futureFertilizer')

    year_from = 2021
    soc_toc_predictions = soc_toc_predictor.predict(coords, year_from)

    current_soc = soc_toc_predictions['SOC'][year_from]
    current_toc = soc_toc_predictions['TOC'][year_from]

    data = {}
    data['percent_increase'] = nutrient_managment_predictor.predict(
        croptype=crop_type,
        current_fertilizer=current_fertilizer,
        future_fertilizer=future_fertilizer,
        current_soc_or_toc=current_soc,
        depth="0-30 cm",
        norm=2
    )

    return jsonify(data)

@app.route('/continuous_cover_impact')
def continuous_cover_impact():
    coords = ast.literal_eval(request.args.get('coords'))
    crop_type = request.args.get('croptype')
    fertilization = request.args.get('fertilization')
    current_continuous_cover = request.args.get('current')
    future_continuous_cover = request.args.get('future')

    year_from = 2021
    soc_toc_predictions = soc_toc_predictor.predict(coords, year_from)

    current_soc = soc_toc_predictions['SOC'][year_from]
    current_toc = soc_toc_predictions['TOC'][year_from]

    data = {}
    data['percent_increase'] = continuous_cover_predictor.predict(
        croptype=crop_type,
        fertilization=fertilization,
        current_continuous_cover=current_continuous_cover,
        future_continuous_cover=future_continuous_cover,
        current_soc_or_toc=current_soc,
        speciestype="Legume & Non-Legume",
        numspecies=2,
        depth="0-30 cm",
        norm=2
    )

    return jsonify(data)

app.run()
