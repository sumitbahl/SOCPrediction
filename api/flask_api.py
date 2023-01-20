from flask import send_file, request, Flask, jsonify
from predict_tillage_impact import TillagePredictor
from predict_TOA_reflectance import SOCTOCPredictor
import ast

app = Flask(__name__)
soc_toc_predictor = SOCTOCPredictor()
tillage_predictor = TillagePredictor()


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


app.run()
