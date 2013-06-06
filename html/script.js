$(document).ready(function()
{
	var mapCenter = [50.25, 10];
	var mapZoom = 6;
	var mapMaxZoom = 12;

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

	var data = _.map(stations["stations"], function (station) {
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
	_.each(stations["stations"], function (station, index, list) {
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
			marker.bindPopup("<strong>"+station["Station Original"]+"</strong>"+"<br>"+station["Fluss"]+"<br>Meldestufe: "+station["Meldestufe Original"]);
			marker.addTo(markerLayer);
		}
	});
	
	var ts = stations["timestamp"].split("-");
	ts = parseInt(ts[2])+"."+parseInt(ts[1])+"."+ts[0]+", "+ts[3]+":"+ts[4]+" Uhr";
	$("#timestamp").html(ts);

	var map = new L.Map('map', {
    	center : mapCenter,
    	zoom : mapZoom,
		layers: [baseLayer, heatmapLayer],
		attributionControl: false
	});
	
	var layerControl = L.control.layers([], {
		"Heatmap": heatmapLayer,
		"Messstationen": markerLayer
	}, {"collapsed": false});
	
	layerControl.addTo(map);
	
	L.control.scale({
		"imperial": false
	}).addTo(map);
});