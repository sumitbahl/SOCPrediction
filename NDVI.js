// Define a point of interest. Use the UI Drawing Tools to import a point
// geometry and name it "point" or set the point coordinates with the
// ee.Geometry.Point() function as demonstrated here.
var rectangle = ee.Geometry.Rectangle([-63, -3.46, -62, -2.46]);

// Import the Landsat 8 TOA image collection.
var l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA');

// Get the least cloudy image in 2015.
var image = ee.Image(
	l8.filterBounds(rectangle)
	.filterDate('2015-01-01', '2015-12-31')
	.sort('CLOUD_COVER')
	.first()
);

// Compute the Normalized Difference Vegetation Index (NDVI).
var nir = image.select('B5');
var red = image.select('B4');
var ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI');

// Display the result.
Map.centerObject(image, 9);
var ndviParams = {min: -1, max: 1, palette: ['blue', 'white', 'green']};
Map.addLayer(ndvi, ndviParams, 'NDVI image');

var meanDict = ndvi.reduceRegion({
	reducer: ee.Reducer.mean(),
	geometry: rectangle,
	scale: 90
});

// Get the mean from the dictionary and print it.
// var mean = meanDict.get('elevation');
print(meanDict.get('NDVI'));