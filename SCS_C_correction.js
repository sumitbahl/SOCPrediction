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