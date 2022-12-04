var illumination = require("users/bahlreyansh/SOC:illumination");

function apply_SCS_C_correction(band, img_plus_ic_mask2) {
	/* Sun-Canopy-Sensor and
		C-correction (SCS+C)
		
		- formula (for each band): 
		𝐿𝐻 = 𝐿𝑇 ⋅ (𝑐o𝑠(s)𝑐o𝑠(θz) + 𝑐) / (IL + 𝑐)
		* 𝐿𝐻 = reflectance of horizontal surface (corrected)
		* 𝐿𝑇 = reflectance of inclined surface (uncorrected)
		* s = terrain slope
		* θz = Zenith angle
		* 𝑐 = intercept of lin reg. / slope of lin reg. where x is IL and y is 𝐿𝑇
		* IL = illumination condition
	*/
	var out = img_plus_ic_mask2.select('IC', band).reduceRegion({
		reducer: ee.Reducer.linearFit(), // Compute coefficients: a(slope), b(intercept), and c(b/a) between 𝐿𝑇 and 𝐼𝐿
		geometry: ee.Geometry(img.geometry().buffer(-500)), // trim off the outer edges of the image for linear relationship
		scale: 300,
		maxPixels: 1000000000
	});

	if (out === null || out === undefined) {
		return img_plus_ic_mask2.select(band);
	}

	// slope
	var a = ee.Number(out.get('scale'));
	
	// intercept
	var b = ee.Number(out.get('offset'));
	
	// C
	var c = b.divide(a);

	// Apply the SCS + C correction
	var SCS_C_output = img_plus_ic_mask2.expression(
		"((LT * (cosB * cosZ + C)) / (IL + C))", {
		'LT': img_plus_ic_mask2.select(band),
		'IL': img_plus_ic_mask2.select('IC'),
		'cosB': img_plus_ic_mask2.select('cosS'),
		'cosZ': img_plus_ic_mask2.select('cosZ'),
		'C': c
	});

	return SCS_C_output;
}

exports.apply_SCS_C_correction = apply_SCS_C_correction;

function correct(img) {

	var img_plus_ic = illumination.illumination(img);

	var mask1 = img_plus_ic.select('B5').gt(-0.1);
	var mask2 = img_plus_ic.select('slope').gte(5)
						.and(img_plus_ic.select('IC').gte(0))
						.and(img_plus_ic.select('B5').gt(-0.1));

	var img_plus_ic_mask2 = ee.Image(img_plus_ic.updateMask(mask2));

	// Specify Bands to topographically correct
	var bandList = ['B2','B3','B4','B5','B6','B7'];
	var compositeBands = img.bandNames();
	var nonCorrectBands = img.select(compositeBands.removeAll(bandList));

	var img_SCS_C_corr = ee.Image(bandList.map(function(x) {
												return apply_SCS_C_correction(x, img_plus_ic_mask2);
											})
											).addBands(img_plus_ic.select('IC'));

	var bandList_IC = ee.List([bandList, 'IC']).flatten();
	img_SCS_C_corr = img_SCS_C_corr.unmask(img_plus_ic.select(bandList_IC)).select(bandList);

	var corrected = img_SCS_C_corr.addBands(nonCorrectBands);

	return corrected;
}

exports.correct = correct;

// testing

var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");

var collection = l8.filterBounds(geometry)
                   .filterDate("2017-01-01","2017-12-31")
                   .sort("CLOUD_COVER")

var img = ee.Image(collection.first());

Map.addLayer(img, {bands: 'B4,B3,B2',min: 0, max: 3000}, 'original');

Map.addLayer(correct(img), {bands: 'B4,B3,B2',min: 0, max: 3000}, 'corrected');
