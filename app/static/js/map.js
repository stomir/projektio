function showGoogleMap(show_self_location, point_list) {
    function init() {
        var mapOptions = {
            center: {lat: 52.069167, lng: 19.480556},
            zoom: 6
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);

        // Lokalizacja użytkownika:
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);

                map.setCenter(pos);
                map.setZoom(11);

                if (show_self_location) {
                    new google.maps.Marker({
                        position: pos,
                        map: map,
                        icon: '/static/img/dot.png'
                    });
                }
            });
        }


        // Wyświetlenie punktów:
        var infowindow = new google.maps.InfoWindow({
            content: ''
        });

        for (var i = 0; i < point_list.length; i++) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(point_list[i].lat, point_list[i].lng),
                map: map,
                title: point_list[i].title
            });

            var infocontent = '<h3>' + point_list[i].title + '</h3><div class="infocontent">' + point_list[i].description + '</div>';

            google.maps.event.addListener(marker, 'click', function (content, point) {
                return function () {
                    infowindow.setContent(content);
                    infowindow.open(map, this);
                    var s = ("#point-" + point.lat + "-" + point.lng).replace(/\./g,"_");
                    $(s).text(travelTime[s]);
                }
            }(infocontent, point_list[i]));
        }
    }

    google.maps.event.addDomListener(window, 'load', init);
}

travelTime = {};
function setDst(sel) {
    return function (response, status) {
        var results = response.rows[0].elements;
        for (var j = 0; j < results.length; j++) {
            var element = results[j];
            $(sel[j]).text(element.duration.text);
            $(sel[j]).data('time', element.duration.text);
            travelTime[sel[j]] = element.duration.text;
        }
    }
}

function initGetTravelTime(point_list, mode) {
    var service = new google.maps.DistanceMatrixService();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var start = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);
            for (var i = 0; i < point_list.length; i += 24) {
                var dests = [];
                var selectors = [];
                for (var j = 0; j < 24 && i + j < point_list.length; j++) {
                    dests.push(new google.maps.LatLng(point_list[i + j].pos.lat, point_list[i + j].pos.lng));
                    selectors.push(point_list[i + j].selector);
                }
                service.getDistanceMatrix(
                    {
                        origins: [start],
                        destinations: dests,
                        travelMode: mode
                    }, setDst(selectors)
                );
            }
        });
    }
}