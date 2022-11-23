var geeSharp = require("users/aazuspan/geeSharp:geeSharp");

// Load a Landsat 8 top-of-atmosphere reflectance image.
var img = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_044034_20140318');

Map.addLayer(
    img,
    {bands: ['B5'], min: 0, max: 0.25, gamma: [1.1]},
    'NIR');
    
// Sharpen B5 (NIR)
var ms = img.select(["B5"]);
// Select the 15 m panchromatic band
var pan = img.select(["B8"]);

// Pan-sharpen
var sharpened = geeSharp.sharpen(ms, pan)
Map.setCenter(-122.44829, 37.76664, 13);
Map.addLayer(sharpened,
             {min: 0, max: 0.25, gamma: [1.3]},
             'pan-sharpened');