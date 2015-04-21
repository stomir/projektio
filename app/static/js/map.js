function showGoogleMap(show_self_location, point_list) {
    function init() {
        var mapOptions = {
            center: {lat: 52.069167, lng: 19.480556},
            zoom: 6
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        console.log(map);

        // Lokalizacja użytkownika:
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);

                map.setCenter(pos);

                if (show_self_location) {
                    new google.maps.Marker({
                        position: pos,
                        map: map,
                        icon: 'dot.png'
                    });
                    console.log("Show self location");
                }
            });
        }


        // Wyświetlenie punktów:
        console.log("Points");
        var infowindow = new google.maps.InfoWindow({
            content: ''
        });

        for (var i = 0; i < point_list.length; i++) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(point_list[i].lat, point_list[i].lng),
                map: map,
                title: point_list[i].title
            });

            var infocontent = '<h3>' + point_list[i].title + '</h3><p>' + point_list[i].description + '</p>';

            google.maps.event.addListener(marker, 'click', function (content) {
                return function () {
                    infowindow.setContent(content);
                    infowindow.open(map, this);
                }
            }(infocontent));
        }

        console.log("Done");
    }

    google.maps.event.addDomListener(window, 'load', init);
    console.log("Added listener");
}