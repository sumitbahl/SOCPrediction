function apply_SCS_C_correction(band) {
	/* Sun-Canopy-Sensor and
		C-correction (SCS+C)
		
		- formula (for each band): 
		𝐿𝐻 = 𝐿𝑇 ⋅ (𝑐o𝑠(s)𝑐o𝑠(θz) + 𝑐) / (IL + 𝑐)
		* 𝐿𝐻 = reflectance of horizontal surface (corrected)
		* 𝐿𝑇 = reflectance of inclined surface (existing)
		* s = terrain slope
		* θz = Zenith angle
		* 𝑐 = intercept of lin reg. / slope of lin reg.
		* IL = illumination condition
	*/
	var out = img_plus_ic_mask2.select('IC', band).reduceRegion({
		reducer: ee.Reducer.linearFit(), // Compute coefficients: a(slope), b(intercept), and c(b/a) between 𝐿𝑇 and 𝐼𝐿
		geometry: ee.Geometry(img.geometry().buffer(-5000)), // trim off the outer edges of the image for linear relationship
		maxPixels: 1000000000
	});

	if (out === null || out === undefined) {
		return img_plus_ic_mask2.select(band);
	}

	else {
		var out_a = ee.Number(out.get('scale'));
		var out_b = ee.Number(out.get('offset'));
		var out_c = out_b.divide(out_a);
		// Apply the SCSc correction
		var SCSc_output = img_plus_ic_mask2.expression(
			"((image * (cosB * cosZ + cvalue)) / (ic + cvalue))", {
			'image': img_plus_ic_mask2.select(band),
			'ic': img_plus_ic_mask2.select('IC'),
			'cosB': img_plus_ic_mask2.select('cosS'),
			'cosZ': img_plus_ic_mask2.select('cosZ'),
			'cvalue': out_c
		});

		return SCSc_output;
	}
}