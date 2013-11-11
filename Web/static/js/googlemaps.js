var geocoder;
var map;

// Initializes map and centers on given coordinates
function initialize() {
	geocoder = new google.maps.Geocoder();
	var latlng = new google.maps.LatLng(37.7577,-122.4376);
	var mapOptions = {
		zoom: 12,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

// Geocoding function
function codeAddress() {
	var address = document.getElementById('address').value;
	geocoder.geocode( {'address':address}, function(results,status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			var marker = new google.maps.Marker({
				map: map,
				position: results[0].geometry.location
			});
		} else {
			alert('Geocode did not work because' + status);
		}
	});
}

google.maps.event.addDomListener(window, 'load', initialize);