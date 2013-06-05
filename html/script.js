$(document).ready(function()
{

    var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/c92a245f75214baa9572bf5e76922113/998/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: mapMaxZoom
    });
	
	var icon1 = L.icon({
	    iconUrl: 'img/1.gif',
	    iconSize: [7, 7],
	    iconAnchor: [3, 3],
	    popupAnchor: [0, 0],
	});
	var icon2 = L.icon({
	    iconUrl: 'img/2.gif',
	    iconSize: [7, 7],
	    iconAnchor: [3, 3],
	    popupAnchor: [0, 0],
	});
	var icon3 = L.icon({
	    iconUrl: 'img/3.gif',
	    iconSize: [7, 7],
	    iconAnchor: [3, 3],
	    popupAnchor: [0, 0],
	});
	var icon4 = L.icon({
	    iconUrl: 'img/4.gif',
	    iconSize: [7, 7],
	    iconAnchor: [3, 3],
	    popupAnchor: [0, 0],
	});

	//var data = _.filter(stations, function (station) {
	//	return parseInt(station["Meldestufe"]) > 0;
	//});
	var data = _.map(stations, function (station) {
		return {
			"lat": station.latitude,
			"lon": station.longitude,
			"value": station["Meldestufe"]
		}
	});
	
	var heatmapLayer = L.TileLayer.heatMap({
		// radius could be absolute or relative
		// absolute: radius in meters, relative: radius in pixels
		radius: { value: 10000, absolute: true },
		opacity: 0.75,
		gradient: {
			0: "rgb(243, 255, 0)",
			0.25: "rgb(255, 166, 0)",
			0.75: "rgb(213, 0, 0)",
			1: "rgb(165, 0, 150)",
		}
	});
	heatmapLayer.setData(data);

	var markerLayer = L.layerGroup();
	_.each(stations, function (station, index, list) {
		if (station.latitude && station.longitude) {
			var icon = null;
			switch (station["Meldestufe"]) {
				case 1:
					icon = icon1;
					break;
				case 2:
					icon = icon2;
					break;
				case 3:
					icon = icon3;
					break;
				case 4:
					icon = icon4;
					break;
				default:
					icon =  new L.Icon.Default();
			}
			var marker = L.marker([station.latitude, station.longitude], {
				"icon": icon
			});
			marker.bindPopup("<strong>"+station["Station Original"]+"</strong>"+"<br>"+station["Fluss"]+"<br>"+station["Meldestufe Original"]+"<br>"+station["latitude"]+","+station["longitude"]+"<br>"+station["Bundesland"]);
			marker.addTo(markerLayer);
		}
	});
	
	var clusterMarkers = new L.MarkerClusterGroup();
	_.each(stations, function (station, index, list) {
		if (station.latitude && station.longitude) {
			var marker = L.marker([station.latitude, station.longitude]);
			marker.bindPopup("<strong>"+station["Station Original"]+"</strong>"+"<br>"+station["Fluss"]+"<br>"+station["Meldestufe Original"]+"<br>"+station["latitude"]+","+station["longitude"]+"<br>"+station["Bundesland"]);
			marker.addTo(clusterMarkers);
		}
	});

	var map = new L.Map('map', {
    	center : mapCenter,
    	zoom : mapZoom,
		layers: [baseLayer, heatmapLayer]
	});
	
	
	L.control.layers([], {
		"Heatmap": heatmapLayer,
		"Stationen": markerLayer,
		"Debug-Marker": clusterMarkers
	}, {"collapsed": false}).addTo(map);
	
	L.control.scale({
		"imperial": false
	}).addTo(map);
	
});