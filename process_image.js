var select_area = require("users/bahlreyansh/SOC:select");
var pan_sharpening = require("users/bahlreyansh/SOC:pan_sharpening");
var topographic_correction = require("users/bahlreyansh/SOC:SCS_C_correction");
var spectral_indices = require("users/bahlreyansh/SOC:spectral_indices");
var data = require("users/bahlreyansh/SOC:data").data;

function process_image(long1, lat1, long2, lat2, MU_GLOBAL) {
	/* Combine selecting area, pan-sharpening, illumination, topographic correction, and spectral indices */

	var img = select_area.select(long1, lat1, long2, lat2);

	img = pan_sharpening.pan_sharpen(img, ["B1", "B2", "B3", "B4", "B5", "B6", "B7","B9", "B10", "B11"]);
	
	// var corrected = topographic_correction.correct(img);

	var indices = spectral_indices.compute_indices(img);

	return indices.set('MU_GLOBAL', MU_GLOBAL);
}

var features = [];

var task = 2;

for (var i = 0; i < 50; i++) {
	var processed = process_image(data[i][1], data[i][3], data[i][2], data[i][4], data[i][0]);
	features.push(ee.Feature(null,processed));
}

Export.table.toDrive(
	ee.FeatureCollection(features),
	"Task" + task,
	"/SOC/Data",
	"" + task
);