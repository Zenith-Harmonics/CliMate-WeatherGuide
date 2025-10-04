document.addEventListener('DOMContentLoaded', function () {

    const mymap = L.map('mapid', {
        center: [51.505, -0.09],
        zoom: 4,
        layers: [
            L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                maxZoom: 17,
                attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
            })
        ]
    });

    marker = L.marker([0, 0]).addTo(mymap);
    mymap.locate({ setView: true, maxZoom: 8 });
    lat = document.getElementById('lat');
    lng = document.getElementById('lng');

    mymap.on('locationfound', function (e) {
        marker = L.marker(e.latlng).addTo(mymap);
        document.getElementById('lat').value = e.latlng.lat.toFixed(6);
        document.getElementById('lng').value = e.latlng.lng.toFixed(6);
    });

    mymap.on('click', function (e) {
        marker.setLatLng(e.latlng);
        document.getElementById('lat').value = e.latlng.lat.toFixed(6);
        document.getElementById('lng').value = e.latlng.lng.toFixed(6);
    });

    lat.addEventListener('change', function () {
        marker.setLatLng([lat.value, lng.value]);
        mymap.setView([lat.value, lng.value], 8);
    });

    lng.addEventListener('change', function () {
        marker.setLatLng([lat.value, lng.value]);
        mymap.setView([lat.value, lng.value], 8);
    });
});