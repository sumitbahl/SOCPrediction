function illumination (img) {
	/* This function calculates the luminous intensity using Lambert's Cosine Law 
	- returns a value between -1 and 1 
	- formula = cos θp cos θz + sin θp sin θz cos (φa - φo) 
	- where: γi = incidence angle
		θp = slope angle
		θz = solar zenith angle = (90 – sun’s elevation angle)
		φa = solar azimuth angle
		φo = aspect angle
	*/
	const DEG_TO_RAD = 3.14159265359 / 180;
	
	// metadata about solar position
	var solar_zenith_angle = ee.Image.constant(ee.Number(img.get('SOLAR_ZENITH_ANGLE'))).multiply(DEG_TO_RAD).clip(img.geometry().buffer(10000));
	var solar_azimuth_angle = ee.Image.constant(ee.Number(img.get('SOLAR_AZIMUTH_ANGLE')).multiply(DEG_TO_RAD)).clip(img.geometry().buffer(10000));
	
	// Creat terrain layers
	var slope = ee.Terrain.slope(dem).clip(img.geometry().buffer(10000));
	var slope_rad = ee.Terrain.slope(dem).multiply(DEG_TO_RAD).clip(img.geometry().buffer(10000));
	var aspect_rad = ee.Terrain.aspect(dem).multiply(DEG_TO_RAD).clip(img.geometry().buffer(10000));

	// Calculate the Illumination Condition
	
	// slope part of the illumination condition
	var cosZ = solar_zenith_angle.cos();
	var cosS = solar_azimuth_angle.cos();
	var slope_illumination = cosS.expression("cosZ * cosS", {'cosZ': cosZ, 'cosS': cosS.select('slope')});

	// aspect part of the illumination condition
	var sinZ = solar_zenith_angle.sin();
	var sinS = slope_rad.sin();
	var cosAziDiff = (solar_azimuth_angle.subtract(aspect_rad)).cos();
	var aspect_illumination = sinZ.expression("sinZ * sinS * cosAziDiff",
		{
			'sinZ': sinZ,
			'sinS': sinS,
			'cosAziDiff': cosAziDiff
		});
	// full illumination condition (IC)
	var ic = slope_illumination.add(aspect_illumination);

	// Add IC to original image
	var img_plus_ic = ee.Image(img.addBands(ic.rename('IC')).addBands(cosZ.rename('cosZ')).addBands(cosS.rename('cosS')).addBands(slope.rename('slope')));
	return img_plus_ic;
}