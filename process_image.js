var select_area = require("users/bahlreyansh/SOC:select");


function process_image(long1, lat1, long2, lat2) {
	/* Combine selecting area, pan-sharpening, illumination, topographic correction, and spectral indices */

	var img = select_area.select(long1, lat1, long2, lat2);
	
}

process_image(-63.937781455384815, -2.8582106566354333, -63.319800498353565, -2.575630995105349);