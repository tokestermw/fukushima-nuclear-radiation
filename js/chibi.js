function initialize() {    
    var map = new google.maps.Map(document.getElementById('map-canvas'), {
	center: new google.maps.LatLng(37.422972, 141.032917),
	zoom: 10,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    
    var layer = new google.maps.FusionTablesLayer({
	query: {
	    select: 'Latitude',
	    from: '1Z7Y_HhPKGagG0pFoKfwDqyNyZYQ7EUgLf9wGUSY'
	},
	
	styles: [{
	    polygonOptions: {
		fillColor: "#00FF00",
		fillOpacity: 0.3
	    }
	}, {
	    markerOptions: {
	 	iconName: "small_green"
	    }
	}]
    });    

    layer.setMap(map);

}

google.maps.event.addDomListener(window, 'load', initialize);
