from flask import send_file, request, Flask, jsonify
from predict_TOA_reflectance import SOCPredictor
import ast

app = Flask(__name__)
soc_predictor = SOCPredictor()

@app.route('/get_data')
def get_data():
	coords = ast.literal_eval(request.args.get('coords'))
	year = int(request.args.get('yearFrom'))
	# soc_predictor.predict(-73., -54.0083333333477, -73.1333333333761, -54.0, 2014)
	data = soc_predictor.predict(coords, year)
	filename = f'img/{str(coords)}{year}.png'
	soc_predictor.plot(data, filename)
	return jsonify(data)

@app.route('/get_plot')
def get_plot():
	coords = ast.literal_eval(request.args.get('coords'))
	year = int(request.args.get('yearFrom'))
	filename = f'img/{str(coords)}{year}.png'
	return send_file(filename, mimetype='image/gif')

app.run()