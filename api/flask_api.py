from flask import send_file, request, Flask, jsonify
from predict_TOA_reflectance import SOCPredictor

app = Flask(__name__)
soc_predictor = SOCPredictor()

@app.route('/get_data')
def get_data():
	long1 = float(request.args.get('long1'))
	long2 = float(request.args.get('long2'))
	lat1 = float(request.args.get('lat1'))
	lat2 = float(request.args.get('lat2'))
	year = int(request.args.get('yearFrom'))
	# soc_predictor.predict(-73., -54.0083333333477, -73.1333333333761, -54.0, 2014)
	data = soc_predictor.predict(long1, lat1, long2, lat2, year)
	filename = f'img/{long1}{lat1}{long2}{lat2}{year}.png'
	soc_predictor.plot(data, filename)
	return jsonify(data)

@app.route('/get_plot')
def get_plot():
	long1 = float(request.args.get('long1'))
	long2 = float(request.args.get('long2'))
	lat1 = float(request.args.get('lat1'))
	lat2 = float(request.args.get('lat2'))
	year = int(request.args.get('yearFrom'))
	filename = f'img/{long1}{lat1}{long2}{lat2}{year}.png'
	return send_file(filename, mimetype='image/gif')

app.run()