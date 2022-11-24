function apply_SCS_C_correction(band) {
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
		geometry: ee.Geometry(img.geometry().buffer(-100)), // trim off the outer edges of the image for linear relationship
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


var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");
 
var inBands = ee.List(['B2','B3','B4','B5','B6','B7'])
var outBands = ee.List(['blue','green','red','nir','swir1','swir2']);
var collection = l8.filterBounds(geometry)
                   .filterDate("2017-01-01","2017-12-31")
                   .sort("CLOUD_COVER")
                   .select(inBands,outBands);
 
var img = ee.Image(collection.first());

var props = img.toDictionary();
var time_start = img.get('system:time_start');

var img_plus_ic = illumination(img);

var mask1 = img_plus_ic.select('nir').gt(-0.1);
var mask2 = img_plus_ic.select('slope').gte(5)
						.and(img_plus_ic.select('IC').gte(0))
						.and(img_plus_ic.select('nir').gt(-0.1));

var img_plus_ic_mask2 = ee.Image(img_plus_ic.updateMask(mask2));

// Specify Bands to topographically correct
var bandList = ['blue','green','red','nir','swir1','swir2'];
var compositeBands = img.bandNames();
print(compositeBands);

var nonCorrectBands = img.select(compositeBands.removeAll(bandList));

var img_SCS_C_corr = ee.Image(bandList.map(apply_SCS_C_correction)).addBands(img_plus_ic.select('IC'));

var bandList_IC = ee.List([bandList, 'IC']).flatten();
img_SCS_C_corr = img_SCS_C_corr.unmask(img_plus_ic.select(bandList_IC)).select(bandList);
print(img_SCS_C_corr);
var corrected = img_SCS_C_corr.addBands(nonCorrectBands);

Map.addLayer(img, {bands: 'red,green,blue',min: 0, max: 3000}, 'original');

Map.addLayer(corrected, {bands: 'red,green,blue',min: 0, max: 3000}, 'corrected');
