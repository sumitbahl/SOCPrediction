var geeSharp = require("users/aazuspan/geeSharp:geeSharp");

function pan_sharpen (img, bands) {
	var ms = img.select(bands);
	// Select the 15 m panchromatic band
	var pan = img.select(["B8"]);

	// Pan-sharpen
	return geeSharp.sharpen(ms, pan);
}


// Testing

// Load a Landsat 8 top-of-atmosphere reflectance image.
var img = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_044034_20140318');

Map.addLayer(
    img.select(["B2", "B3", "B4"]),
    {},
    'Orig');
    
var sharpened = pan_sharpen(img, ["B2", "B3", "B4"]);

Map.setCenter(-122.44829, 37.76664, 13);
Map.addLayer(sharpened,
             {},
             'pan-sharpened');