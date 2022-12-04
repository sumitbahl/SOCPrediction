var geeSharp = require("users/aazuspan/geeSharp:geeSharp");

function pan_sharpen (img, bands) {
	var to_sharpen = img.select(bands);
	// Select the 15 m panchromatic band
	var pan = img.select(["B8"]);

	// Pan-sharpen
	return geeSharp.sharpen(to_sharpen, pan).addBands(pan);
}

exports.pan_sharpen = pan_sharpen;

// Testing

// Load a Landsat 8 top-of-atmosphere reflectance image.
// var img = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_044034_20140318');

// Map.addLayer(
//     img.select(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B9", "B10", "B11"]),
//     {},
//     'Orig');
    
// var sharpened = pan_sharpen(img, ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B9", "B10", "B11"]);

// Map.setCenter(-122.44829, 37.76664, 13);
// Map.addLayer(sharpened,
//              {},
//              'pan-sharpened');