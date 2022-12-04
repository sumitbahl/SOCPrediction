function select(long1, lat1, long2, lat2) {
	var rectangle = ee.Geometry.Rectangle([long1, lat1, long2, lat2]);

	var dataset = 'LANDSAT/LC08/C01/T1_TOA';

	var l8 = ee.ImageCollection(dataset);

	var img = ee.Image(
		l8.filterBounds(rectangle)
			.filterDate('2015-01-01',
				'2015-12-31')
			.sort('CLOUD_COVER').first()
	);
	return img.clip(rectangle);
}
// testing
// var img = select(-63.937781455384815, -2.8582106566354333, -63.319800498353565, -2.575630995105349);
// Map.addLayer(img, {}, "sample selection" )

exports.select = select;
