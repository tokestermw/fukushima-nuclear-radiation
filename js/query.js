// Adapted after Robin Kraft
// http://www.reddmetrics.com/2011/08/10/fusion-tables-javascript-query-maps.html
// http://jsfiddle.net/odi86/Sbt2P/

function demoinit() {

    // Centered on Indonesia
    var latlon = new google.maps.LatLng(37.422972, 141.032917);

    var options = {
        disableDefaultUI: true,
        zoom: 10,
        center: latlon,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: true,
        scaleControl: true,
        zoomControl: true
    };

    mymap = new google.maps.Map(document.getElementById("map-canvas"), options);

    getData('1jl5I-8zA1Ijt1wEUYLmB4ji3de5YzHMi_IpfgKI');
}

function getData(table) {
    // Builds a Fusion Tables SQL query and hands the result to dataHandler()

    //var queryUrlHead = 'http://www.google.com/fusiontables/api/query?sql=';
    var queryUrlHead = 'https://www.googleapis.com/fusiontables/v1/query?sql=';

    var queryUrlTail = '&key=AIzaSyAq4M53XkVSjRwNweNooYwsyaSOWKeHWws';

    //var queryUrlTail = '&jsonCallback=?'; // ? could be a function name
    
    //var pickedDate = '2011-11-01';
    var pickedDate = document.getElementById('datepicker').value;

    // write your SQL as normal, then encode it
    var query = "SELECT Radiation, Latitude, Longitude, Date FROM " + table + 
	" WHERE Date = '" + pickedDate + "'";
    var queryurl = encodeURI(queryUrlHead + query + queryUrlTail);

    console.log(queryurl);

    jqxhr = $.get(queryurl, dataHandler, "jsonp");
}


function dataHandler(d) {
    // get the actual data out of the JSON object
    var data = d.rows;
    console.log(data);
    infoWindow = new google.maps.InfoWindow();

    // heatmap data
    var heatmapData = [];

    // loop through all rows to add them to the map
    for (var i = 0; i < data.length; i++) {
        // Per the expected data format [25,-7.854167,131.3026], 
        // lat is stored in d[row][1] and lon is stored in d[row][2]
        // probability is the first element of the array
        var latlon = new google.maps.LatLng(data[i][1], data[i][2]);
        var probability = data[i][0];

        // var marker = new google.maps.Marker({
        //     position: latlon,
        //     rowid: i,
        //     prob: probability,
        //     map: mymap,
	//     icon: getCircle(probability)
        // });

        // var fn = markerClick(mymap, marker, infoWindow);
        // google.maps.event.addListener(marker, 'click', fn);

	var weightedLoc = {
	    location: latlon,
	    weight: probability	    
	};

	heatmapData.push(weightedLoc);

    }

    var heatmap = new google.maps.visualization.HeatmapLayer({
	data: heatmapData,
	dissipating: true,
	opacity: .8,
	radius: 20,
	map: mymap
    });

}

function getCircle(magnitude) {
    var circle = {
	path: google.maps.SymbolPath.CIRCLE,
	fillColor: 'red',
	fillOpacity: .0,
	scale: Math.pow(2, magnitude),
	strokeColor: 'white',
	strokeWeight: 0
    };
    return circle;
}

function markerClick(map, m, ifw) {
    return function() {
        // In case there's already an infoWindow open
        ifw.close(map)
        
        // Build html content, using data stored in the marker instance
        var infoHtml = '<strong>rowid: '+ m.rowid + ' prob: ' + m.prob
        infoHtml += '</strong><br />' + m.position.toString() + "</p>";

        // Standard infoWindow initialization steps
        infoWindow.setContent(infoHtml);
        infoWindow.setPosition(m.position);
        infoWindow.open(map);
    };
}

//demoinit();
google.maps.event.addDomListener(window, 'load', demoinit);
