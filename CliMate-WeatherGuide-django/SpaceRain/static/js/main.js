window.onload = init;

function init() {
    const mymap = L.map('mapid',{
        center: [51.505, -0.09],
        zoom: 4,
        layers: [
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            })
        ]
    });
}