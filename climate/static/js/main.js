document.addEventListener('DOMContentLoaded', function () {

    const mymap = L.map('mapid', {
        center: [51.505, -0.09],
        zoom: 4,
        layers: [
            L.tileLayer('https://tile.jawg.io/jawg-dark/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
	attribution: '<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	minZoom: 0,
	maxZoom: 22,
	accessToken: '5SbJYIvyrKNfQ7WsBgES4QMGjneZYUMXUUd0CucB2Ain0RtkfHMBgkGVrHQtSJOY'
})
        ]
    });

    // marker = L.marker([0, 0]).addTo(mymap);
    mymap.locate({ setView: true, maxZoom: 8 });
    lat = document.getElementById('lat');
    lng = document.getElementById('lng');

    mymap.on('locationfound', function (e) {
        marker = L.marker(e.latlng).addTo(mymap);
        document.getElementById('lat').value = e.latlng.lat.toFixed(6);
        document.getElementById('lng').value = e.latlng.lng.toFixed(6);
    });

    mymap.on('locationerror', function (e) {
        marker = L.marker([51.505, -0.09]).addTo(mymap);
        document.getElementById('lat').value = 51.505.toFixed(6);
        document.getElementById('lng').value = (-0.09).toFixed(6);
        alert("Could not get your location");
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